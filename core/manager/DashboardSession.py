class DashboardSession:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DashboardSession, cls).__new__(cls)
            cls._instance._data = {
                "services_status":{"database": 0,"webserver": 0,"redis":0},
                "start_all_services": 0
            }
        return cls._instance

    def set(self,key,value):
        self._data[key] = value

    def get(self,key, default=None):
        return self._data.get(key,default)

    def add_to_current_key(self,top_level_key, key_to_add, value_to_add):
        if top_level_key in self._data:
            target_dict = self._data[top_level_key]
            if isinstance(target_dict, dict):
                target_dict[key_to_add] = value_to_add
                return True
        return False

    def delete(self, key):
        if key in self._data:
            del self._data[key]

    def clear(self):
        self._data.clear()