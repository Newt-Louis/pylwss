from core.repository import WebserverRepository
from core.database.model import WebserverSetting
from core.manager.EventBus import EventBus
from core.services import ConfigGeneratorService, SynchronizationService

class WebserverCoreService:
    webserver_repository = WebserverRepository

    def __init__(self):
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

    def start_nginx_service(self,language,data):
        if language == 'php':
            project_data = {
                "project_name": "my-laravel-app",
                "domain": "my-laravel-app.test",
                "http_port": 80,
                "ssl_port": 443,
                "is_ssl_enabled": True,
                "ssl_certificate_path": "C:/laragon-clone/ssl/my-laravel-app.crt",
                "ssl_key_path": "C:/laragon-clone/ssl/my-laravel-app.key",
                "document_root": "C:/laragon-clone/www/my-laravel-app/public",
                "access_log_path": "C:/laragon-clone/logs/nginx/my-laravel-app.access.log",
                "error_log_path": "C:/laragon-clone/logs/nginx/my-laravel-app.error.log",

                # ---- Dữ liệu quan trọng ----
                "project_type": "static_php",  # Báo cho template đây là project PHP
                "php_fpm_socket": "127.0.0.1:9001"  # Cổng PHP-FPM của bản PHP 8.1
            }
        else:
            project_data = {
                "project_name": "my-node-api",
                "domain": "my-node-api.test",
                "http_port": 80,
                "ssl_port": 443,
                "is_ssl_enabled": False,
                # (bỏ qua các biến ssl_*)

                # Document root vẫn cần cho Nginx, dù không phải là ưu tiên
                "document_root": "C:/laragon-clone/www/my-node-api",
                "access_log_path": "C:/laragon-clone/logs/nginx/my-node-api.access.log",
                "error_log_path": "C:/laragon-clone/logs/nginx/my-node-api.error.log",

                # ---- Dữ liệu quan trọng ----
                "project_type": "proxy",  # Báo cho template đây là project Proxy
                "app_port": 8001  # Cổng mà app Node đang chạy (do bạn gán)
            }
        ConfigGeneratorService.generate_config_file(
            template_name='nginx_vhost.j2',
            context=project_data,
            output_path='C:/laragon-clone/nginx/conf/sites-enabled/my-laravel-app.conf'
        )