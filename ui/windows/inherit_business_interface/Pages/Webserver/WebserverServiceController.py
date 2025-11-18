from core.services import webserver_core_service

class WebserverServiceController:
    def __init__(self):
        self.webserver_core_service = webserver_core_service

    def save_changes(self,data: dict) -> bool:
        return True if self.webserver_core_service.save_settings(data) else False

    def cancel_changes(self):
        print("Webserver Page Controller _on_cancel_changes")

    def add_new_data(self):
        print("Webserver Page Controller _on_add_new_data")

    def update_data(self):
        print("Webserver Page Controller _on_update_data")

    def load_data(self):
        try:
            settings_data = self.webserver_core_service.load_settings()
            return None if settings_data is None else settings_data
        except Exception as e:
            print(e)
            raise

    def load_webservers_version(self):
        return self.webserver_core_service.load_webservers_versions()