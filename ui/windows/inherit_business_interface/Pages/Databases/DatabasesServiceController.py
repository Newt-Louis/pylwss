from core.services.databases.DatabaseCoreService import DatabaseCoreService

class DatabasesServiceController:
    def __init__(self):
        self.database_core_service = DatabaseCoreService()

    def _on_save_changes(self):
        print("Dashboard Page Controller _on_save_changes")

    def _on_cancel_changes(self):
        print("Dashboard Page Controller _on_cancel_changes")

    def _on_add_new_data(self):
        print("Dashboard Page Controller _on_add_new_data")

    def _on_update_data(self):
        print("Dashboard Page Controller _on_update_data")

    def _on_load_data(self):
        print("Dashboard Page Controller _on_load_data")