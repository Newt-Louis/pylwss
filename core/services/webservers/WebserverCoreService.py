import os, subprocess
from core.repository import WebserverRepository
from core.database.model import WebserverSetting
from core.manager.EventBus import EventBus
from core.services import ConfigGeneratorService, SynchronizationService
from core.config import config

CREATE_NO_WINDOW = 0x08000000

class WebserverCoreService:
    webserver_repository = WebserverRepository

    def __init__(self):
        self.nginx_process: subprocess.Popen | None = None
        self.apache_process: subprocess.Popen | None = None
        pass

    # noinspection PyUnresolvedReferences
    def load_settings(self) -> list[WebserverSetting] | None:
        print(f"SERVICE: Đang tải cấu hình...")
        try:
            settings_data = self.__class__.webserver_repository.get_all_webserver_settings()
            return None if settings_data is None else settings_data
        except:
            raise

    def save_settings(self, settings_data: dict) -> bool:
        try:
            model_data = {
                'server_name': settings_data.get('type'),
                'selected_version': settings_data.get('selected_version'),
                'executable_path': settings_data.get('executable_path'),
                'sites_enabled_path': settings_data.get('sites_enabled_path'),
                'tld_template': settings_data.get('tld') if settings_data.get('tld') else '.test',
                'http_port': settings_data.get('listen_port'),
                'ssl_port': None,
                'alp_path': settings_data.get('access_log_path'),
                'elp_path': settings_data.get('error_log_path'),
                'is_enabled': True
            }
            setting_model = WebserverSetting(**model_data)

            if not self.webserver_repository.disable_all_webservers():
                raise Exception

            success = self.__class__.webserver_repository.update_webserver_settings(setting_model)

            if success:
                print(f"SERVICE: Đã lưu thành công cho {setting_model.server_name}.")
                EventBus.webserver_saved.emit(setting_model.__dict__)
                if setting_model.server_name == 'nginx':
                    ConfigGeneratorService.regenerate_main_nginx_config(setting_model)
                elif setting_model.server_name == 'apache':
                    ConfigGeneratorService.regenerate_main_apache_config(setting_model)

            current_webserver_data = WebserverCoreService.webserver_repository.get_all_webserver_settings(model_data["server_name"])
            if current_webserver_data[0].tld_template != model_data["tld"]:
                WebserverCoreService.webserver_repository.update_tld_in_database(model_data["tld"])
                SynchronizationService.sync_update_tld_workflow(model_data["tld"])

            return success
        except Exception as e:
            print(f"SERVICE ERROR: {e}")
            return False

    def load_webservers_versions(self):
        return self.__class__.webserver_repository.get_all_webserver_versions()

    def start_nginx_service(self,settings: WebserverSetting):
        print("NGINX SERVICE: Đang khởi động dịch vụ...")
        exec_path = self._get_executable_path(settings, 'nginx')

        if self.nginx_process and self.nginx_process.poll() is None:
            # EventBus.log_received.emit("Nginx đã chạy từ trước.")
            return
        if not self._test_nginx_config(exec_path):
#             EventBus.log_received.emit("Khởi động Nginx thất bại: File cấu hình có lỗi.")
            return
        nginx_dir = self._get_base_path(exec_path, 'nginx')
        self.nginx_process = subprocess.Popen([exec_path], cwd=nginx_dir, creationflags=CREATE_NO_WINDOW)
#         EventBus.log_received.emit(f"Nginx đã khởi động (PID: {self.nginx_process.pid})")
#         EventBus.service_status_changed.emit("nginx", "running")

    def stop_nginx_service(self, settings: WebserverSetting):
        print("NGINX SERVICE: Đang dừng...")
        exec_path = self._get_executable_path(settings, 'nginx')
        nginx_dir = self._get_base_path(exec_path, 'nginx')

        subprocess.run([exec_path, "-s", "stop"], cwd=nginx_dir, creationflags=CREATE_NO_WINDOW)

        if self.nginx_process:
            self.nginx_process.wait(timeout=5)
        self.nginx_process = None
#         EventBus.log_received.emit("Nginx đã dừng.")
#         EventBus.service_status_changed.emit("nginx", "stopped")

    def reload_nginx_service(self, settings: WebserverSetting):
        print("NGINX SERVICE: Đang tải lại...")
        exec_path = self._get_executable_path(settings, 'nginx')

        if not self._test_nginx_config(exec_path):
#             EventBus.log_received.emit("Tải lại Nginx thất bại: File cấu hình có lỗi.")
            return

        nginx_dir = self._get_base_path(exec_path, 'nginx')
        subprocess.run([exec_path, "-s", "reload"], cwd=nginx_dir, creationflags=CREATE_NO_WINDOW)
#         EventBus.log_received.emit("Nginx đã tải lại cấu hình.")

    # noinspection PyMethodMayBeStatic
    def _test_nginx_config(self, executable_path: str) -> bool:
        """Chạy 'nginx -t' để kiểm tra file config."""
        nginx_dir = self._get_base_path(executable_path, 'nginx')
        try:
            # Dùng subprocess.run() vì ta MUỐN đợi nó chạy xong
            # và kiểm tra kết quả
            result = subprocess.run([executable_path, "-t"],cwd=nginx_dir, capture_output=True, text=True,
                encoding='utf-8', creationflags=CREATE_NO_WINDOW)

            if result.returncode == 0:
                print("NGINX SERVICE: Cấu hình OK.")
                return True
            else:
                print(f"NGINX SERVICE LỖI: Cấu hình sai.\n{result.stderr}")
                # EventBus.log_received.emit(f"Nginx Config Error:\n{result.stderr}")
                return False
        except Exception as e:
            print(f"Lỗi khi kiểm tra config nginx: {e}")
            # EventBus.log_received.emit(f"Lỗi khi chạy 'nginx -t': {e}")
            return False

    def start_apache_service(self, settings: WebserverSetting):
        print("APACHE SERVICE: Đang khởi động...")
        exec_path = self._get_executable_path(settings, 'apache')

        if self.apache_process and self.apache_process.poll() is None:
#             EventBus.log_received.emit("Apache đã chạy từ trước.")
            return

        if not self._test_apache_config(exec_path):
#             EventBus.log_received.emit("Khởi động Apache thất bại: File cấu hình có lỗi.")
            return

        # Apache dùng Popen với lệnh -k start
        apache_dir = self._get_base_path(exec_path, 'apache')
        self.apache_process = subprocess.Popen([exec_path, "-k", "start"], cwd=apache_dir,
                                               creationflags=CREATE_NO_WINDOW)
#         EventBus.log_received.emit(f"Apache đã khởi động (PID: {self.apache_process.pid})")
#         EventBus.service_status_changed.emit("apache", "running")

    def stop_apache_service(self, settings: WebserverSetting):
        print("APACHE SERVICE: Đang dừng...")
        exec_path = self._get_executable_path(settings, 'apache')
        apache_dir = self._get_base_path(exec_path, 'apache')

        # Dùng -k shutdown (an toàn) hoặc -k stop
        subprocess.run([exec_path, "-k", "shutdown"], cwd=apache_dir, creationflags=CREATE_NO_WINDOW)

        if self.apache_process:
            self.apache_process.wait(timeout=5)
        self.apache_process = None
#         EventBus.log_received.emit("Apache đã dừng.")
#         EventBus.service_status_changed.emit("apache", "stopped")

    def reload_apache_service(self, settings: WebserverSetting):
        print("APACHE SERVICE: Đang tải lại...")
        exec_path = self._get_executable_path(settings, 'apache')

        if not self._test_apache_config(exec_path):
            EventBus.log_received.emit("Tải lại Apache thất bại: File cấu hình có lỗi.")
            return

        # Apache dùng -k restart để tải lại
        apache_dir = self._get_base_path(exec_path, 'apache')
        subprocess.run([exec_path, "-k", "restart"], cwd=apache_dir, creationflags=CREATE_NO_WINDOW)
#         EventBus.log_received.emit("Apache đã tải lại cấu hình.")

    def _test_apache_config(self, executable_path: str) -> bool:
        apache_dir = self._get_base_path(executable_path, 'apache')
        try:
            result = subprocess.run([executable_path, "-t"], cwd=apache_dir, capture_output=True, text=True,
                                    encoding='utf-8', creationflags=CREATE_NO_WINDOW)
            if "Syntax OK" in result.stderr:  # Apache báo OK ở stderr
                print("APACHE SERVICE: Cấu hình OK.")
                return True
            else:
#                 EventBus.log_received.emit(f"Apache Config Error:\n{result.stderr}")
                return False
        except Exception as e:
            print(f"Lỗi khi kiểm tra config apache: {e}")
#             EventBus.log_received.emit(f"Lỗi khi chạy 'httpd.exe -t': {e}")
            return False

    # noinspection PyMethodMayBeStatic
    def _get_executable_path(self, settings: WebserverSetting, server_type: str) -> str:
        db_path = settings.executable_path
        if db_path and os.path.exists(db_path):
            return db_path

        fallback_path = ""
        if server_type == 'nginx':
            fallback_path = os.path.join(str(config.NGINX_ROOT), 'nginx-1.28.0', 'nginx.exe')
        elif server_type == 'apache':
            fallback_path = os.path.join(str(config.APACHE_ROOT), 'httpd-2.4.63-250207-win64-VS17', 'bin', 'httpd.exe')

        if fallback_path and os.path.exists(fallback_path):
            print(f"SERVICE: Không tìm thấy đường dẫn DB, dùng fallback: {fallback_path}")
            return fallback_path

        # Nếu cả hai đều không có, báo lỗi
        raise FileNotFoundError(
            f"Không tìm thấy file thực thi cho {server_type} tại '{db_path}' hoặc '{fallback_path}'")

    # noinspection PyMethodMayBeStatic
    def _get_base_path(self, executable_path: str, server_type: str)->str:
        """Lấy thư mục làm việc (cwd)"""
        if server_type == 'nginx':
            # từ: D:/nginx/nginx.exe -> D:/nginx
            return os.path.dirname(executable_path)
        elif server_type == 'apache':
            # từ D:/apache24/bin/httpd.exe -> D:/apache24
            return os.path.dirname(os.path.dirname(executable_path))
        else:
            raise ValueError(f"Unsupported server type: {server_type}")