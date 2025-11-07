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
        data_dir = Path(self.settings.base_data_path)

        if not data_dir.exists():
            error_msg = f"Lỗi: Thư mục data '{data_dir}' không tồn tại."
            print(error_msg)
            raise FileNotFoundError(error_msg)

        if not self.base_conf_path.exists():
            is_empty = not any(data_dir.iterdir())
            if not is_empty:
                error_msg = f"Thư mục data '{data_dir}' không trống nhưng thiếu file 'postgresql.conf' quan trọng. Vui lòng chọn thư mục trống."
                print(error_msg)
                raise Exception(error_msg)

            print(f"Thư mục data trống. Đang chạy initdb cho PostgreSQL...")
            initdb_path = self._get_executable_path("initdb.exe")

            # -U postgres: tạo user superuser mặc định tên 'postgres'
            # --no-locale -E UTF8: cài đặt mã hóa chuẩn, tránh lỗi
            init_command = [str(initdb_path), "-D", str(data_dir), "-U", "postgres", "--no-locale", "-E", "UTF8"]

            try:
                subprocess.run(init_command, check=True, capture_output=True, text=True, encoding="utf-8",
                               errors="ignore")
            except subprocess.CalledProcessError as e:
                print(f"Lỗi nghiêm trọng khi chạy initdb: {e.stderr}")
                raise

            print("initdb hoàn tất.")

        self._generate_app_conf()
        self._create_user_conf_if_needed()

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

    def _get_executable_path(self, exe_name: str = "pg_ctl.exe") -> str:
        path = Path(self.settings.root_path) / "bin" / exe_name
        if not path.exists():
            raise FileNotFoundError(f"Không tìm thấy file: {path}")
        return str(path)

    def _get_pg_ctl_command(self, action: str) -> list:
        pg_ctl_path = self._get_executable_path('pg_ctl.exe')
        data_dir = self.settings.base_data_path

        # -l (logfile): Chỉ định file log
        base_cmd = [str(pg_ctl_path), action, "-D", str(data_dir), "-l", str(data_dir / "logfile.log")]

        if action == "start":
            # nạp nhiều file config
            # -o (options) được truyền thẳng tới server `postgres`
            # Thứ tự là quan trọng: base -> app -> user (user ghi đè tất cả)
            options = f"-c config_file='{self.base_conf_path.as_posix()}' " \
                      f"-c config_file='{self.app_conf_path.as_posix()}' " \
                      f"-c config_file='{self.user_conf_path.as_posix()}'"

            base_cmd.extend(["-o", options])

        return base_cmd

    def _generate_app_conf(self):
        content = f"""
            # =================================================================
            # AUTOMATIC CONFIGURATION FILE BY PYWSSL
            # CHANGES WILL BE OVERWRITE
            # =================================================================
            port = {self.settings.port}
            listen_addresses = '127.0.0.1'
        """
        try:
            with open(self.app_conf_path, "w", encoding="utf-8") as f:
                f.write(content)
        except IOError as e:
            print(f"Lỗi ghi {self.app_conf_path}: {e}")
            raise

    def _create_user_conf_if_needed(self):
        if self.user_conf_path.exists():
            return

        content = """
            # =================================================================
            # USER CUSTOM CONFIGURATION FILE
            # =================================================================
            #
            # Thêm các thiết lập PostgreSQL của riêng bạn tại đây.
            # Ví dụ:
            #
            # max_connections = 200
            # shared_buffers = '256MB'
            #
        """
        try:
            with open(self.user_conf_path, "w", encoding="utf-8") as f:
                f.write(content)
        except IOError as e:
            print(f"Lỗi tạo {self.user_conf_path}: {e}")