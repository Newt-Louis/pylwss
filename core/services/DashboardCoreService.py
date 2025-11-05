from core.database.model import DashboardSetting
from core.repository import DashboardRepository,WebserverRepository
from core.services.webservers.WebserverCoreService import WebserverCoreService
from core.manager.EventBus import EventBus

class DashboardCoreService:
    dashboard_repository = DashboardRepository
    webserver_repository = WebserverRepository
    def __init__(self):
        self.webserver_core_service = WebserverCoreService
        EventBus.app_exit.connect(self.reset_dashboard_statuses)

    def get_init_dashboard_info(self)->list[DashboardSetting] | None:
        try:
            dashboard_info = self.dashboard_repository.get_all_dashboard_settings()
            return dashboard_info if dashboard_info else None
        except Exception as e:
            raise e

    def webserver_service_handler(self,status):
        try:
            settings = self.webserver_repository.get_current_webserver()
            print(settings)
        except Exception as e:
            print(f"DASHBOARD SERVICE: Lỗi khi lấy cài đặt: {e}")
            EventBus.log_received.emit(f"Lỗi DB: {e}")
            return

        if not settings:
            print("DASHBOARD SERVICE: Không tìm thấy webserver nào đang được kích hoạt.")
            EventBus.log_received.emit("Lỗi: Chưa cấu hình webserver.")
            return

            # Bước 2: Điều phối dựa trên server_name
        server_name = settings.server_name.lower()

        try:
            if server_name == 'nginx':
                if status == 1:
                    self.webserver_core_service.start_nginx_service(settings)
                elif status == 0:
                    self.webserver_core_service.stop_nginx_service(settings)
                elif status == 'reload':
                    self.webserver_core_service.reload_nginx_service(settings)

            elif server_name == 'apache':
                if status == 1:
                    self.webserver_core_service.start_apache_service(settings)
                elif status == 0:
                    self.webserver_core_service.stop_apache_service(settings)
                elif status == 'reload':
                    self.webserver_core_service.reload_apache_service(settings)

            else:
                print(f"DASHBOARD SERVICE: Webserver '{server_name}' không được hỗ trợ.")
                EventBus.log_received.emit(f"Lỗi: Webserver '{server_name}' không được hỗ trợ.")

        except Exception as e:
            # Bắt các lỗi chung (ví dụ: FileNotFoundError từ CoreService)
            print(f"DASHBOARD SERVICE: Lỗi khi thực thi lệnh '{status}': {e}")
            EventBus.log_received.emit(f"Lỗi nghiêm trọng: {e}")

    def update_webserver_dashboard(self, data: dict):
        dashboard_setting = DashboardSetting(**dict(data))
        self.dashboard_repository.save_webserver(dashboard_setting)

    def update_language_dashboard(self, data: dict):
        dashboard_setting = DashboardSetting(**dict(data))
        self.dashboard_repository.save_language(dashboard_setting)

    def update_database_dashboard(self, data: dict):
        dashboard_setting = DashboardSetting(**dict(data))
        self.dashboard_repository.save_database(dashboard_setting)

    def update_tools_dashboard(self, data: dict):
        self.dashboard_repository.save_tool(data)

    def update_network_dashboard(self, data: dict):
        self.dashboard_repository.save_network(data)

    def reset_dashboard_statuses(self):
        self.dashboard_repository.reset_dashboard_statuses()