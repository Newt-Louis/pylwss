from core.services import DashboardCoreService


class DashboardServiceController:
    def __init__(self):
        self.dashboard_core_service = DashboardCoreService()

    def on_start_webserver(self):
        print("dashboards Page Controller _on_save_changes")


    def on_start_database(self):
        print("dashboards Page Controller _on_cancel_changes")

    def on_start_language(self):
        print("dashboards Page Controller _on_add_new_data")

    def on_start_tools(self):
        print("dashboards Page Controller _on_update_data")

    def on_start_network(self):
        print("dashboards Page Controller _on_load_data")

    def update_webserver_info(self, data: dict):
        print("dashboards Page Controller _update_webserver_info")

    def update_database_info(self, data: dict):
        print("dashboards Page Controller _update_webserver_info")

    def update_language_info(self, data: dict):
        print("dashboards Page Controller _update_webserver_info")

    def update_tool_info(self, data: dict):
        print("dashboards Page Controller _update_webserver_info")

    def update_network_info(self, data: dict):
        print("dashboards Page Controller _update_webserver_info")