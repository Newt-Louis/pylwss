from core.services import DashboardCoreService
from core.services.tools import ToolsCoreService
from core.database.model import DashboardSetting
from core.utils import Helper

class DashboardServiceController:
    def __init__(self):
        self.dashboard_core_service = DashboardCoreService()
        self.tools_core_service = ToolsCoreService()

    def handle_on_load_init_dashboard_info(self)->list[DashboardSetting] | None:
        try:
            dashboard_info = self.dashboard_core_service.get_init_dashboard_info()
            return dashboard_info if dashboard_info else None
        except Exception as e:
            raise e

    def handle_on_webserver_service(self,status):
        try:
            self.dashboard_core_service.webserver_service_handler(status)
        except:
            raise

    def handle_on_database_service(self,status):
        try:
            return self.dashboard_core_service.databases_service_handler(status)
        except:
            raise

    def handle_on_language_service(self):
        print("dashboards Page Controller _on_add_new_data")

    def handle_on_tools_service(self,tools_toggle_info):
        if "redis" in tools_toggle_info:
            if tools_toggle_info["redis"] == 1:
                self.tools_core_service.start_redis_service()
            else:
                self.tools_core_service.stop_redis_service()


    def handle_on_network_service(self):
        print("dashboards Page Controller _on_load_data")

    def update_webserver_info(self, data: dict):
        webserver_info = {
            "service": data["service"],
            "type": data["server_name"],
            "version": data["selected_version"],
            "is_running": data["is_running"],
        }
        self.dashboard_core_service.update_webserver_dashboard(webserver_info)

    def update_database_info(self, data: dict):
        database_info = {
            "service": data["service"],
            "type": data["type"],
            "version": Helper.get_last_segment(data["root_path"]),
            "is_running": data["is_running"],
        }
        self.dashboard_core_service.update_database_dashboard(database_info)

    def update_language_info(self, data: dict):
        language_info = {
            "service": data["service"],
            "type": data["language"],
            "version": data["selected_version"],
            "is_running": data["is_running"],
        }
        self.dashboard_core_service.update_language_dashboard(language_info)

    def update_tool_info(self, data: dict):
        print("dashboards Page Controller _update_webserver_info")

    def update_network_info(self, data: dict):
        print("dashboards Page Controller _update_webserver_info")