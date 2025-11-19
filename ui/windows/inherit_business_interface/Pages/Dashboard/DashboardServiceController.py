from core.services import dashboard_core_service
from core.services import tools_core_service
from core.database.model import DashboardSetting
from core.utils import Helper

class DashboardServiceController:
    def __init__(self):
        self.dashboard_core_service = dashboard_core_service

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

    def handle_on_redis_service(self,status):
        if status:
            try:
                result = tools_core_service.start_redis_service()
                if not result["status"]:
                    return result
            except:
                raise
        else:
            tools_core_service.stop_redis_service()


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