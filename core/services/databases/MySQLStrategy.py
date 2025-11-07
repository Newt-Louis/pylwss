import subprocess,os
from .DatabaseServiceStrategy import DatabaseServiceStrategy
from core.database.model import DatabaseSetting
from pathlib import Path


class MySQLStrategy(DatabaseServiceStrategy):

    def __init__(self, settings: DatabaseSetting):
        super().__init__(settings)
        self.ini_path = Path(self.settings.root_path) / "mysql.ini"
        self.user_ini_path = Path(self.settings.root_path) / "user.ini"

    def initialize_if_needed(self):
        self._generate_ini_file()
        self._create_user_ini_if_needed()

        data_dir = Path(self.settings.base_data_path)
        if data_dir.exists():
            if not any(data_dir.iterdir()):
                mysqld_path = self._get_executable_path("mysqld.exe")
                init_command = [
                    str(mysqld_path),
                    f"--defaults-file={self.ini_path}",
                    "--initialize-insecure"
                ]
                try:
                    subprocess.run(init_command, check=True, capture_output=True, text=True)
                    print("Khởi tạo MySQL (initialize-insecure) hoàn tất.")
                except subprocess.CalledProcessError as e:
                    print("Lỗi nghiêm trọng khi khởi tạo MySQL:")
                    print(f"STDOUT: {e.stdout}")
                    print(f"STDERR: {e.stderr}")
                    raise
                except FileNotFoundError as e:
                    print(f"Lỗi: {e}")
                    raise
            else:
                print("Thư mục data đã có dữ liệu, không khởi tạo")
        else:
            raise FileNotFoundError("Thư mục data không tồn tại")

    def get_start_command(self) -> list:
        mysqld_path = self._get_executable_path("mysqld.exe")
        return [
            mysqld_path,
            f"--defaults-file={self.ini_path}",
            "--console"
        ]

    def _get_executable_path(self, exe_name: str = "mysqld.exe") -> str:
        path = Path(self.settings.root_path) / "bin" / exe_name
        if not path.exists():
            raise FileNotFoundError(f"Không tìm thấy file: {path}")
        return str(path)

    def _generate_ini_file(self):
        datadir_str = Path(self.settings.base_data_path).as_posix()
        basedir_str = Path(self.settings.root_path).as_posix()
        os.makedirs(self.settings.root_path, exist_ok=True)
        ini_content = f"""
            # =========================================================
            # THIS FILE IS AUTOMATICALLY MANAGED BY YOUR APPLICATION
            # ANY DIRECT CHANGES WILL BE OVERWRITE.
            #
            # TO ADD CUSTOM CONFIGURATIONS, EDIT THE 'user.ini' FILE
            # =========================================================
            [mysqld]
            basedir = "{basedir_str}"
            datadir = "{datadir_str}"
            port = {self.settings.port}
            bind-address = 127.0.0.1
            default_authentication_plugin = mysql_native_password
            sql_mode = "NO_ENGINE_SUBSTITUTION"
                
            [client]
            port = {self.settings.port}
            default-character-set = utf8mb4
            plugin-dir = "{Path(self.settings.root_path).as_posix()}/lib/plugin"
                
            !include user.ini
        """
        try:
            with open(self.ini_path, "w", encoding="utf-8") as f:
                f.write(ini_content)
        except IOError as e:
            print(f"Lỗi khi ghi file .ini: {e}")
            raise

    def _create_user_ini_if_needed(self):
        if self.user_ini_path.exists():
            return  # Không làm gì nếu file đã tồn tại

        user_ini_content = """
            # =================================================================
            # USER CONFIGURATION FILE
            # =================================================================
            #
            # Add your own MySQL settings here.
            # Ví dụ:
            #
            # [mysqld]
            # ssl-ca = "C:/path/to/ca.pem"
            # ssl-cert = "C:/path/to/server-cert.pem"
            # ssl-key = "C:/path/to/server-key.pem"
            #
            # max_connections = 200
            #
        """
        try:
            with open(self.user_ini_path, "w", encoding="utf-8") as f:
                f.write(user_ini_content)
        except IOError as e:
            print(f"Lỗi khi tạo file {self.user_ini_path}: {e}")
