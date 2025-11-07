from abc import ABC, abstractmethod
from core.database.model import DatabaseSetting

class IDatabaseServiceStrategy(ABC):
    """
        Lớp cơ sở trừu tượng (ABC) cho mọi chiến lược dịch vụ CSDL.

        Cung cấp logic chung để BẮT ĐẦU và DỪNG một tiến trình con.
        Bắt buộc các lớp con phải định nghĩa logic riêng cho việc
        khởi tạo và lấy lệnh khởi động.
        """
    def __init__(self,settings:DatabaseSetting):
        self.settings = settings

    @abstractmethod
    def initialize_if_needed(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass