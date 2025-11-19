from core.services import tools_core_service

class ToolsServiceController:
    def __init__(self, tools_model=None):
        self.tools_core_service = tools_core_service

    def on_save_changes(self,**kwargs):
        list_settings = []
        for key, value in kwargs.items():
            if isinstance(value, dict) and value:
                value['type'] = key
                list_settings.append(value)
        try:
            return self.tools_core_service.save_tools_config(list_settings)
        except:
            raise

    def on_cancel_changes(self):
        print("Tools Page Controller _on_cancel_changes")

    def on_add_new_data(self):
        print("Tools Page Controller _on_add_new_data")

    def on_update_data(self):
        print("Tools Page Controller _on_update_data")

    def on_load_data(self):
        try:
            tools_settings = self.tools_core_service.get_init_tools_settings()
            return [tool_settings.model_dump() for tool_settings in tools_settings]
        except:
            raise
