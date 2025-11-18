from core.database.model import DashboardSetting
from core.repository import DashboardRepository,WebserverRepository,DatabaseRepository
from core.services.webservers.WebserverCoreService import webserver_core_service
from core.services.databases.DatabaseCoreService import database_core_service
from core.manager.EventBus import event_bus

class DashboardCoreService:
    def __init__(self):
        self.webserver_core_service = webserver_core_service
        self.database_core_service = database_core_service
        event_bus.app_exit.connect(self.reset_dashboard_statuses)

    def get_init_dashboard_info(self)->list[DashboardSetting] | None:
        try:
            dashboard_info = DashboardRepository.get_all_dashboard_settings()
            return dashboard_info if dashboard_info else None
        except Exception as e:
            raise e

    def webserver_service_handler(self,status):
        try:
            settings = WebserverRepository.get_current_webserver()
            print(settings)
        except Exception as e:
            print(f"DASHBOARD SERVICE: Lỗi khi lấy cài đặt: {e}")
            event_bus.log_received.emit(f"Lỗi DB: {e}")
            return

        if not settings:
            print("DASHBOARD SERVICE: Không tìm thấy webserver nào đang được kích hoạt.")
            event_bus.log_received.emit("Lỗi: Chưa cấu hình webserver.")
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
                event_bus.log_received.emit(f"Lỗi: Webserver '{server_name}' không được hỗ trợ.")

        except Exception as e:
            # Bắt các lỗi chung (ví dụ: FileNotFoundError từ CoreService)
            print(f"DASHBOARD SERVICE: Lỗi khi thực thi lệnh '{status}': {e}")
            event_bus.log_received.emit(f"Lỗi nghiêm trọng: {e}")

    def databases_service_handler(self,status):
        if status == 1:
            try:
                self.database_core_service.start_current_service()
            except:
                raise
        elif status == 0:
            try:
                self.database_core_service.stop_current_service()
            except:
                raise

    def update_webserver_dashboard(self, data: dict):
        dashboard_setting = DashboardSetting(**dict(data))
        DashboardRepository.save_webserver(dashboard_setting)

    def update_language_dashboard(self, data: dict):
        dashboard_setting = DashboardSetting(**dict(data))
        DashboardRepository.save_language(dashboard_setting)

    def update_database_dashboard(self, data: dict):
        dashboard_setting = DashboardSetting(**dict(data))
        DashboardRepository.save_database(dashboard_setting)

    def update_tools_dashboard(self, data: dict):
        DashboardRepository.save_tool(data)

    def update_network_dashboard(self, data: dict):
        DashboardRepository.save_network(data)

    def reset_dashboard_statuses(self):
        DashboardRepository.reset_dashboard_statuses()

dashboard_core_service = DashboardCoreService()