class ServiceContainer:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServiceContainer, cls).__new__(cls)
            cls._instance.services = {}
        return cls._instance

    def register(self, name: str, service_instance):
        print(f"Đăng ký dịch vụ: {name}")
        self.services[name] = service_instance

    def get(self, name: str):
        try:
            return self.services[name]
        except KeyError:
            raise Exception(f"Dịch vụ '{name}' chưa được đăng ký.")

    # Tạo Singleton ngay lập tức
Container = ServiceContainer()