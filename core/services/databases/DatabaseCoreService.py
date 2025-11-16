import os, subprocess
from pathlib import Path
from core.database.model import DatabaseSetting
from core.config import config
from core.repository import DatabaseRepository
from .MySQLStrategy import MySQLStrategy
from .PostgreSQLStrategy import PostgreSQLStrategy
from .IDatabaseServiceStrategy import IDatabaseServiceStrategy
from core.manager.EventBus import event_bus

class DatabaseCoreService:
    def __init__(self):
        self._DB_SERVICES_PATH = config.DB_SERVICES
        self._active_services: dict[str, IDatabaseServiceStrategy] = {}

        event_bus.app_exit.connect(self._listener_app_exit)

    #noinspection PyMethodMayBeStatic
    def get_all_database_settings(self) -> list[DatabaseSetting]:
        try:
            return DatabaseRepository.get_all_database_settings()
        except:
            raise

    def save_settings_and_initialize(self, settings: dict):
        """
        Đây là hàm quan trọng cho trang Cài đặt.
        Nó LƯU cấu hình và CHẠY KHỞI TẠO, nhưng KHÔNG start server.
        """
        try:
            setting_model = DatabaseSetting(**settings)
            DatabaseRepository.reset_database_statuses()

            DatabaseRepository.save_database_setting(setting_model)

            strategy = self._get_strategy_factory(setting_model)
            if not strategy:
                raise Exception(f"Không tìm thấy chiến lược cho {setting_model.type}")

            strategy.initialize_if_needed()

            print(f"Hoàn tất thiết lập cho {setting_model.type}. Sẵn sàng để khởi động từ Dashboard.")
            event_bus.database_saved.emit(setting_model.model_dump())
            return True

        except FileNotFoundError as e:
            print(f"Lỗi đường dẫn: {e}. Vui lòng kiểm tra lại 'Đường dẫn gốc'.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"Lỗi khi chạy tiến trình CSDL: {e}")
            return False
        except Exception as e:
            print(f"Lỗi không xác định khi lưu và khởi tạo: {e}")
            return False

    def start_current_service(self)->bool:
        """
        Bật CSDL hiện tại (được đánh dấu is_chosen = 1).
        Hàm này được gọi từ Dashboard.
        """
        print("Đang tìm CSDL được chọn để khởi động...")
        settings = DatabaseRepository.get_current_database_setting()

        if not settings:
            print("Không có CSDL nào được chọn. Vui lòng vào Cài đặt.")
            return False

        service_name = f"{settings.type}_{settings.port}"
        if service_name in self._active_services:
            print(f"{service_name} đã chạy rồi.")
            return False

        print(f"Đang khởi động {service_name}...")
        strategy = self._get_strategy_factory(settings)
        if not strategy:
            return False

        try:
            if strategy.start():  # Hàm start() đến từ lớp base
                self._active_services[service_name] = strategy
                print(f"{service_name} đã khởi động thành công.")
                return True
            else:
                print(f"Lỗi: Không thể khởi động {service_name}.")
                return False
        except:
            raise

    def stop_current_service(self)->bool:
        settings = DatabaseRepository.get_current_database_setting()
        if not settings:
            print("Không có CSDL nào được chọn.")
            return False

        service_name = f"{settings.type}_{settings.port}"
        strategy = self._active_services.get(service_name)

        if not strategy:
            print(f"{service_name} không có trong danh sách đang chạy.")
            return False

        try:
            if strategy.stop():
                del self._active_services[service_name]
                return True
            else:
                print(f"Lỗi: Không thể dừng {service_name}.")
                return False
        except:
            raise

    def stop_all_services(self):
        # Cần copy list() vì dict sẽ thay đổi kích thước khi lặp
        for service_name in list(self._active_services.keys()):
            strategy = self._active_services.get(service_name)
            if strategy:
                strategy.stop()

        self._active_services.clear()

    # noinspection PyMethodMayBeStatic
    def _get_strategy_factory(self, settings: DatabaseSetting) -> IDatabaseServiceStrategy | None:
        """
        Sử dụng loại strategy database tương ứng
        """
        db_type = settings.type.lower()

        if db_type == "mysql":
            return MySQLStrategy(settings)

        if db_type == "postgresql":
           return PostgreSQLStrategy(settings)

        print(f"Lỗi: Loại CSDL '{db_type}' chưa được hỗ trợ.")
        return None

    def _listener_app_exit(self):
        self.stop_all_services()

database_core_service = DatabaseCoreService()