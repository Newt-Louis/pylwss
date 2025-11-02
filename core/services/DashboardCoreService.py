from core.repository import DashboardRepository

class DashboardCoreService:
    dashboard_repository = DashboardRepository
    def __init__(self):
        pass

    def start_webserver_service(self):
        print("gọi lệnh chạy subprocess bắt đầu dịch vụ web")