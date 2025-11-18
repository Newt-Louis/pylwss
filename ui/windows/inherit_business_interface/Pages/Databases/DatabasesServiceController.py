from core.services.databases.DatabaseCoreService import database_core_service

class DatabasesServiceController:
    def __init__(self):
        self.database_core_service = database_core_service

    def save_changes(self,setting:dict):
        try:
            return self.database_core_service.save_settings_and_initialize(setting)
        except:
            raise

    def cancel_changes(self):
        print("Dashboard Page Controller _on_cancel_changes")

    def add_new_data(self):
        print("Dashboard Page Controller _on_add_new_data")

    def update_data(self):
        print("Dashboard Page Controller _on_update_data")

    def load_data(self)->list[dict]:
        try:
            database_settings = self.database_core_service.get_all_database_settings()
            return [database_setting.model_dump() for database_setting in database_settings] if database_settings else None
        except:
            raise
