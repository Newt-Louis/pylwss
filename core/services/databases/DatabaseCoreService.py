import os, subprocess
from pathlib import Path
from core.database.model import DatabaseSetting
from core.config import config
from core.repository import DatabaseRepository
from .MySQLStrategy import MySQLStrategy
from .DatabaseServiceStrategy import DatabaseServiceStrategy

class DatabaseCoreService:
    def __init__(self):
        self._DB_SERVICES_PATH = config.DB_SERVICES
        self._active_services: dict[str, DatabaseServiceStrategy] = {}

    def save_settings(self,settings: DatabaseSetting):
        print("Chuẩn bị lưu cấu hình database")

    def save_settings_and_initialize(self, settings: DatabaseSetting):
        """
        Đây là hàm quan trọng cho trang Cài đặt.
        Nó LƯU cấu hình và CHẠY KHỞI TẠO, nhưng KHÔNG start server.
        """
        try:
            DatabaseRepository.reset_database_statuses()

            settings.is_chosen = True

            DatabaseRepository.save_database_setting(settings)

            strategy = self._get_strategy_factory(settings)
            if not strategy:
                raise Exception(f"Không tìm thấy chiến lược cho {settings.type}")

            strategy.initialize_if_needed()

            print(f"Hoàn tất thiết lập cho {settings.type}. Sẵn sàng để khởi động từ Dashboard.")
            return True

        except FileNotFoundError as e:
            print(f"Lỗi đường dẫn: {e}. Vui lòng kiểm tra lại 'Đường dẫn gốc'.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"Lỗi khi chạy tiến trình CSDL: {e.stderr}")
            return False
        except Exception as e:
            print(f"Lỗi không xác định khi lưu và khởi tạo: {e}")
            return False

    def start_current_service(self):
        """
        Bật CSDL hiện tại (được đánh dấu is_chosen = 1).
        Hàm này được gọi từ Dashboard.
        """
        print("Đang tìm CSDL được chọn để khởi động...")
        settings = DatabaseRepository.get_current_database_setting()

        if not settings:
            print("Không có CSDL nào được chọn. Vui lòng vào Cài đặt.")
            return

        service_name = f"{settings.type}_{settings.port}"
        if service_name in self._active_services:
            print(f"{service_name} đã chạy rồi.")
            return

        print(f"Đang khởi động {service_name}...")
        strategy = self._get_strategy_factory(settings)
        if not strategy:
            return

        if strategy.start():  # Hàm start() đến từ lớp base
            self._active_services[service_name] = strategy
            print(f"{service_name} đã khởi động thành công.")
        else:
            print(f"Lỗi: Không thể khởi động {service_name}.")

    def stop_current_service(self):
        """Dừng CSDL hiện tại đang chạy."""
        settings = DatabaseRepository.get_current_database_setting()
        if not settings:
            print("Không có CSDL nào được chọn.")
            return

        service_name = f"{settings.type}_{settings.port}"
        strategy = self._active_services.get(service_name)

        if not strategy:
            print(f"{service_name} không có trong danh sách đang chạy.")
            return

        print(f"Đang dừng {service_name}...")
        if strategy.stop():  # Hàm stop() đến từ lớp base
            del self._active_services[service_name]
            print(f"{service_name} đã dừng.")
        else:
            print(f"Lỗi: Không thể dừng {service_name}.")

    def stop_all_services(self):
        """Dừng tất cả các dịch vụ khi tắt ứng dụng."""
        print("Đang dừng tất cả các dịch vụ...")
        # Cần copy list() vì dict sẽ thay đổi kích thước khi lặp
        for service_name in list(self._active_services.keys()):
            strategy = self._active_services.get(service_name)
            if strategy:
                strategy.stop()

        self._active_services.clear()
        print("Tất cả dịch vụ đã dừng.")

    # noinspection PyMethodMayBeStatic
    def _get_strategy_factory(self, settings: DatabaseSetting) -> DatabaseServiceStrategy | None:
        """
        Sử dụng loại strategy database tương ứng
        """
        db_type = settings.type.lower()

        if db_type == "mysql":
            return MySQLStrategy(settings)

        # if db_type == "postgresql":
        #    return PostgreSQLStrategy(settings)

        print(f"Lỗi: Loại CSDL '{db_type}' chưa được hỗ trợ.")
        return None