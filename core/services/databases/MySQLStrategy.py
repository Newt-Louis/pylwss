import subprocess, os, time
from .IDatabaseServiceStrategy import IDatabaseServiceStrategy
from core.database.model import DatabaseSetting
from pathlib import Path


class MySQLStrategy(IDatabaseServiceStrategy):

    def __init__(self, settings: DatabaseSetting):
        super().__init__(settings)
        self.ini_path = Path(self.settings.root_path) / "mysql.ini"
        self.user_ini_path = Path(self.settings.root_path) / "user.ini"
        self.process: subprocess.Popen | None = None

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
                    subprocess.run(init_command, check=True, capture_output=True, text=True, cwd=Path(self.settings.root_path))
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

    def start(self) -> bool:
        if self.process:
            return True

        command = self._get_start_command()
        working_directory = Path(self.settings.root_path)
        if not working_directory.exists():
            raise FileNotFoundError("Thư mục gốc mysql không tồn tại")

        try:
            self.process = subprocess.Popen(command,cwd=working_directory,
                                            stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,
                                            text=True,encoding='utf-8',errors='ignore')

            time.sleep(2.0)  # Chờ 2s
            exit_code = self.process.poll()
            if exit_code is not None:
                error_message = self.process.stderr.read()
                print(f"LỖI: {self.settings.type} không thể khởi động: {error_message}")
                self.process = None
                return False

            return True
        except Exception as e:
            print(f"Lỗi khi khởi động {self.settings.type}: {e}")
            self.process = None
            return False

    def stop(self) -> bool:
        if not self.process:
            print(f"{self.settings.type} chưa chạy.")
            return True

        try:
            admin_path = self._get_executable_path("mysqladmin.exe")
            shutdown_command = [
                str(admin_path),
                "-u", "root",
                "--protocol=TCP",
                f"--port={self.settings.port}",
                "shutdown"
            ]
            subprocess.run(shutdown_command,check=True,capture_output=True,
                            timeout=10,cwd=Path(self.settings.root_path))
            if self.process:
                self.process.wait(timeout=10)

            self.process.terminate()
            self.process.wait(timeout=5)
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            try:
                # Dùng taskkill để giết cả TIẾN TRÌNH CHA VÀ CON (/T)
                pid_to_kill = self.process.pid
                kill_command = [
                    "taskkill",
                    "/PID", str(pid_to_kill),
                    "/T",  # <-- /T (Tree) sẽ giết cả tiến trình con
                    "/F"  # /F (Force)
                ]
                subprocess.run(kill_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.process.wait(timeout=2)
            except Exception as kill_e:
                print(f"Lỗi khi ép dừng: {kill_e}")
                # Thử kill lần cuối
                if self.process: self.process.kill()
        except Exception as e:
            print(f"Lỗi khi dừng {self.settings.type}: {e}")
            return False
        finally:
            self.process = None

        return True

    def _get_start_command(self) -> list:
        mysqld_path = self._get_executable_path("mysqld.exe")
        return [
            mysqld_path,
            f"--defaults-file={self.ini_path}",
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
        ini_content = f"""# =========================================================
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

        user_ini_content = """# =================================================================
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
#"""
        try:
            with open(self.user_ini_path, "w", encoding="utf-8") as f:
                f.write(user_ini_content)
        except IOError as e:
            print(f"Lỗi khi tạo file {self.user_ini_path}: {e}")
