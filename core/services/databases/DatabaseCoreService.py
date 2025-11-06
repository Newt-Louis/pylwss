import os, subprocess
from pathlib import Path
from core.database.model import DatabaseSetting
from core.config import config
from core.repository import DatabaseRepository

class DatabaseCoreService:
    def __init__(self):
        self._DB_SERVICES_PATH = config.DB_SERVICES
        self._mysql_process = None

    def save_settings(self,settings: DatabaseSetting):
        print("Chuẩn bị lưu cấu hình database")

    def generate_ini_file(self,type):
        if type == "mysql":
            mysql_template = self.mysql_template()
        else:
            print("Chưa có DBMS này trong ứng dụng, cần cài đặt thêm!")

    def mysql_template(self, settings):
        settings = {
            "port":3306,
            "data_directory": self._DB_SERVICES_PATH / "mysql-8.4.6-winx64" / "data",
            "sql_mode":"NO_ENGINE_SUBTITUTION",
            "auth_plugin":"mysql_native_password",
        }
        datadir = settings['data_directory'].replace('\\', '/')
        ini_content = f""" 
                            [mysqld]
                            port = {settings['port']}
                            datadir = "{datadir}"
                            bind-address = 127.0.0.1
                            default_authentication_plugin = {settings['auth_plugin']}
                            sql_mode = "{settings['sql_mode']}"
                        """
        config_path = self._DB_SERVICES_PATH / "mysql-8.4.6-winx64" /  "mysql.ini"
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(ini_content)
            print(f"Tạo file {config_path} thành công!")
        except IOError as e:
            print(f"Lỗi khi ghi file: {e}")

    def setup_new_mysql_instance(self, settings: DatabaseSetting, service_name: str, root_password: str):
        """
        Hàm trọn gói để thiết lập một phiên bản MySQL mới.
        """

        data_dir = Path(settings.data_directory)
        ini_path = self._DB_SERVICES_PATH / "mysql-8.4.6-winx64" / "mysql.ini"  # Hoặc lấy từ generate_ini_file

        try:
            # Bước 1: Tạo file .ini (Giả sử hàm này đã được gọi trước đó)
            # self.generate_ini_file(settings)
            # print(f"Đã tạo file {ini_path}")

            # Bước 2: Khởi tạo (Chỉ khi thư mục data không tồn tại)
            if not data_dir.exists():
                print("Thư mục 'data' không tồn tại. Đang khởi tạo MySQL...")
                # Sử dụng --initialize-insecure để tạo root@localhost không cần mật khẩu
                init_command = [
                    str(self._MYSQLD_PATH),
                    f"--defaults-file={ini_path}",
                    "--initialize-insecure"
                ]
                subprocess.run(init_command, check=True, capture_output=True, text=True)
                print("Khởi tạo MySQL thành công.")
            else:
                print("Thư mục 'data' đã tồn tại. Bỏ qua bước khởi tạo.")

            # Bước 3: Cài đặt Dịch vụ Windows
            print(f"Đang cài đặt dịch vụ Windows với tên: {service_name}")
            # Xóa dịch vụ cũ nếu có, phòng trường hợp cài đặt lỗi trước đó
            subprocess.run(["sc", "delete", service_name], capture_output=True)

            install_command = [
                str(self._MYSQLD_PATH),
                f"--defaults-file={ini_path}",
                "--install",
                service_name
            ]
            subprocess.run(install_command, check=True, capture_output=True, text=True)
            print(f"Cài đặt dịch vụ {service_name} thành công.")

            # Bước 4: Khởi động Dịch vụ
            print(f"Đang khởi động dịch vụ {service_name}...")
            start_command = ["net", "start", service_name]
            subprocess.run(start_command, check=True, capture_output=True, text=True)
            print(f"Dịch vụ {service_name} đã khởi động.")

            # Bước 5: Đặt mật khẩu Root
            print("Đang đặt mật khẩu root...")
            # Câu lệnh SQL để đổi mật khẩu
            sql_command = f"ALTER USER 'root'@'localhost' IDENTIFIED BY '{root_password}';"

            set_pass_command = [
                str(self._MYSQL_PATH),
                "-u", "root",
                "--skip-password",  # Vì root chưa có mật khẩu
                "-P", str(settings.port),
                "-e", sql_command
            ]
            subprocess.run(set_pass_command, check=True, capture_output=True, text=True)
            print("Đặt mật khẩu root thành công!")

            print("Hoàn tất thiết lập MySQL!")
            return True

        except subprocess.CalledProcessError as e:
            print(f"Đã xảy ra lỗi trong quá trình thiết lập MySQL:")
            print(f"Lệnh: {' '.join(e.cmd)}")
            print(f"Lỗi (stdout): {e.stdout}")
            print(f"Lỗi (stderr): {e.stderr}")
            # Cân nhắc thêm logic dọn dẹp ở đây (ví dụ: net stop, sc delete)
            return False
        except Exception as e:
            print(f"Đã xảy ra lỗi không mong muốn: {e}")
            return False

    def start_service(self, service_name: str):
        if self._mysql_process:
            print("MySQL đã chạy rồi.")
            return
        # Đường dẫn đến file thực thi
        mysqld_path = self._MYSQL_BIN_PATH / "mysqld.exe"

        command = [
            str(mysqld_path),
            f"--defaults-file={ini_path}"
        ]
        try:
            self._mysql_process = subprocess.Popen(command,
                                                   stdout=subprocess.DEVNULL,
                                                   stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Lỗi khi khởi động dịch vụ: {e.stderr}")

    def stop_service(self, service_name: str):
        """Dừng một dịch vụ đang chạy."""
        try:
            self._mysql_process.terminate()  # Gửi tín hiệu dừng
            self._mysql_process.wait(timeout=10)  # Chờ tối đa 10s
        except subprocess.TimeoutExpired as e:
            print(f"Lỗi khi dừng dịch vụ: {e.stderr}")
            self._mysql_process.kill()
        except Exception as e:
            print(f"Lỗi khi dừng dịch vụ: {e}")
        finally:
            self._mysql_process = None

    def remove_service(self, service_name: str):
        """Gỡ bỏ một dịch vụ khỏi Windows."""
        try:
            # Đảm bảo dịch vụ đã dừng trước khi gỡ bỏ
            self.stop_service(service_name)
        except Exception:
            pass  # Bỏ qua nếu dịch vụ đã dừng rồi

        try:
            print(f"Đang gỡ bỏ dịch vụ {service_name}...")
            subprocess.run(["sc", "delete", service_name], check=True, capture_output=True, text=True)
            print(f"Dịch vụ {service_name} đã được gỡ bỏ.")
        except subprocess.CalledProcessError as e:
            print(f"Lỗi khi gỡ bỏ dịch vụ: {e.stderr}")