import subprocess
from abc import ABC, abstractmethod
from core.database.model import DatabaseSetting
from pathlib import Path

class DatabaseServiceStrategy(ABC):
    """
        Lớp cơ sở trừu tượng (ABC) cho mọi chiến lược dịch vụ CSDL.

        Cung cấp logic chung để BẮT ĐẦU và DỪNG một tiến trình con.
        Bắt buộc các lớp con phải định nghĩa logic riêng cho việc
        khởi tạo và lấy lệnh khởi động.
        """
    def __init__(self,settings:DatabaseSetting, base_path: Path):
        self.settings = settings
        self.base_path = base_path
        self.process: subprocess.Popen | None = None

    @abstractmethod
    def get_executable_path(self):
        pass

    @abstractmethod
    def initialize_if_needed(self):
        pass

    @abstractmethod
    def get_start_command(self):
        pass

    def start(self):
        if self.process:
            print(f"{self.settings.db_type} đã chạy rồi.")
            return True

        try:
            self.initialize_if_needed()
        except Exception as e:
            print(f"LỖI khi khởi tạo service database {self.settings.db_type}: {e}")
            return False

        command = self.get_start_command()

        try:

            self.process = subprocess.Popen(command,
                                            stdout=subprocess.DEVNULL,
                                            stderr=subprocess.PIPE)

            # TODO: Cần thêm một bước kiểm tra xem tiến trình có lỗi
            # ngay lập tức không (vd: port đã sử dụng).
            # self.process.poll() / self.process.stderr.read()

            return True
        except Exception as e:
            print(f"Lỗi khi khởi động service database {self.settings.db_type}: {e}")
            self.process = None
            return False

    def stop(self):
        if not self.process:
            print(f"{self.settings.db_type} chưa chạy.")
            return True

        try:
            self.process.terminate()  # Gửi tín hiệu yêu cầu dừng
            self.process.wait(timeout=10)  # Chờ 10s
        except subprocess.TimeoutExpired:
            self.process.kill()  # Ép dừng
        except Exception as e:
            return False
        finally:
            self.process = None

        return True