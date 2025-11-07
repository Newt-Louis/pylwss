import subprocess
from .IDatabaseServiceStrategy import IDatabaseServiceStrategy
from core.database.model import DatabaseSetting
from pathlib import Path


class PostgreSQLStrategy(IDatabaseServiceStrategy):

    def __init__(self, settings: DatabaseSetting):
        super().__init__(settings)
        self.app_conf_path = Path(self.settings.root_path) / "app.conf"
        self.user_conf_path = Path(self.settings.root_path) / "user.conf"
        self.base_conf_path = Path(self.settings.base_data_path) / "postgresql.conf"

    def initialize_if_needed(self):
        pass

    def start(self) -> bool:
        try:
            self.initialize_if_needed()

            command = self._get_pg_ctl_command("start")
            # Chạy và chờ, vì pg_ctl sẽ thoát ngay
            result = subprocess.run(command, check=True, capture_output=True, text=True)

            # Kiểm tra trạng thái
            status_command = self._get_pg_ctl_command("status")
            status_result = subprocess.run(status_command, capture_output=True, text=True)

            if "server is running" in status_result.stdout:
                print("PostgreSQL đã khởi động thành công.")
                return True
            else:
                print(f"LỖI: Không thể khởi động PostgreSQL. Log: {status_result.stdout}")
                return False

        except Exception as e:
            print(f"Lỗi khi khởi động PostgreSQL: {e}")
            return False

    def stop(self) -> bool:
        try:
            command = self._get_pg_ctl_command("stop")
            subprocess.run(command, check=True, capture_output=True)
            print("PostgreSQL đã dừng.")
            return True
        except Exception as e:
            print(f"Lỗi khi dừng PostgreSQL: {e}")
            return False

    def _get_pg_ctl_command(self, action: str) -> list:
        pg_ctl_path = self._get_executable_path('pg_ctl.exe')
        data_dir = self.settings.base_data_path
        return [str(pg_ctl_path), action, "-D", str(data_dir)]

    def _get_executable_path(self, exe_name: str = "pg_ctl.exe") -> str:
        path = Path(self.settings.root_path) / "bin" / exe_name
        if not path.exists():
            raise FileNotFoundError(f"Không tìm thấy file: {path}")
        return str(path)