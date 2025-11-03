from core.repository import DashboardRepository

class DashboardCoreService:
    dashboard_repository = DashboardRepository
    def __init__(self):
        pass

    def webserver_service_handler(self,status):
        print("gọi lệnh chạy subprocess bắt đầu dịch vụ web")