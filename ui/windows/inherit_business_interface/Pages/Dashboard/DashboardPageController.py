from PySide6.QtWidgets import QWidget, QMessageBox
from core.manager.Logger import logger
from .DashboardServiceController import DashboardServiceController
from ui.windows.origin_interface import Ui_DashboardPage
from core.manager.EventBus import event_bus
from core.manager.DashboardSession import DashboardSession


class DashboardPageController(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.ui = Ui_DashboardPage()
        self.ui.setupUi(self)
        self.dashboard_service = DashboardServiceController()
        self.dashboard_session = DashboardSession()

        dashboard_infos = self.dashboard_service.handle_on_load_init_dashboard_info()
        if dashboard_infos is not None:
            for dashboard_info in dashboard_infos:
                match dashboard_info.service:
                    case "language":
                        self.ui.language_type_label.setText(dashboard_info.type)
                        self.ui.language_version_label.setText(dashboard_info.version)
                    case "database":
                        self.ui.database_type_label.setText(dashboard_info.type)
                        self.ui.database_version_label.setText(dashboard_info.version)
                    case "webserver":
                        self.ui.webserver_type_label.setText(dashboard_info.type)
                        self.ui.webserver_version_label.setText(dashboard_info.version)
                    case "tool":
                        print("Tools tạm thời chưa phát triển thêm")

        # Nghe sự kiện phát ra từ các trang dịch vụ khác
        event_bus.webserver_saved.connect(self.listener_webserver_saved)
        event_bus.language_saved.connect(self.listener_language_saved)
        event_bus.database_saved.connect(self.listener_database_saved)
        event_bus.tools_saved.connect(self.listener_tool_saved)
        event_bus.log_received.connect(lambda data: self.handle_on_log_received(data))
        event_bus.service_status_changed.connect(lambda data: self.handle_on_status_changed(data))

        # Gán hàm xử lý sự kiện cho nút start all
        self.ui.startall_button.clicked.connect(self.switch_state_all_services)
        self.ui.webserver_start_pushButton.clicked.connect(self.switch_state_webserver)
        self.ui.database_start_pushButton.clicked.connect(self.switch_state_database)
        self.ui.language_start_pushButton.clicked.connect(self.reload_language)
        self.ui.tool_redis_start_pushButton.clicked.connect(self.switch_state_redis)
        # self.ui.tool_mailsender_start_pushButton.clicked.connect() Chờ phát triển
        # self.ui.tool_notepadpp_start_pushButton.clicked.connect()  Chờ phát triển
        self.ui.network_start_pushButton.clicked.connect(self.switch_state_network)

    def switch_state_all_services(self):
        start_all_status = self.dashboard_session.get("start_all_services")
        if start_all_status == 0:
            self.dashboard_session.set("start_all_services", 1)
            self.ui.startall_button.setText("Stop")
        else:
            self.dashboard_session.set("start_all_services", 0)
            self.ui.startall_button.setText("Start All")

    def switch_state_database(self):
        database_status = self.dashboard_session.get("services_status")
        if "database" in database_status:
            match database_status["database"]:
                case 0:
                    self.ui.database_start_pushButton.setText("Stop")
                    self.dashboard_session.add_to_current_key("services_status", "database", 1)
                    self.dashboard_service.handle_on_database_service(1)
                case 1:
                    self.ui.database_start_pushButton.setText("Start")
                    self.dashboard_session.add_to_current_key("services_status", "database", 0)
                    self.dashboard_service.handle_on_database_service(0)
            data_to_save = {
                "service": "database",
                "type": self.ui.database_type_label.text(),
                "root_path":self.ui.database_version_label.text(),
                "is_running": database_status["database"]
            }
            self.dashboard_service.update_database_info(data_to_save)

    def switch_state_webserver(self):
        webserver_status = self.dashboard_session.get("services_status")
        if "webserver" in webserver_status:
            match webserver_status["webserver"]:
                case 0:
                    self.ui.webserver_start_pushButton.setText("Stop")
                    self.dashboard_session.add_to_current_key("services_status", "webserver", 1)
                    self.dashboard_service.handle_on_webserver_service(1)
                case 1:
                    self.ui.webserver_start_pushButton.setText("Start")
                    self.dashboard_session.add_to_current_key("services_status","webserver",0)
                    self.dashboard_service.handle_on_webserver_service(0)

            data_to_save = {
                "service": "webserver",
                "server_name": self.ui.webserver_type_label.text(),
                "selected_version": self.ui.webserver_version_label.text(),
                "is_running": webserver_status["webserver"],
            }
            self.dashboard_service.update_webserver_info(data_to_save)

    def switch_state_redis(self):
        redis_status = self.dashboard_session.get("services_status")["redis"]
        try:
            if redis_status:
                self.dashboard_service.handle_on_redis_service(0)
            else:
                result = self.dashboard_service.handle_on_redis_service(1)
                if not result["status"]:
                    QMessageBox.warning(self, "Warning", result["message"])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Lỗi bật dịch vụ Redis {e}")

    def reload_language(self):
        language_status = self.dashboard_session.get("services_status")
        if "language" in language_status:
            print("Đã có trạng thái dịch vụ language --> chuyển đổi trạng thái")
        else:
            self.dashboard_session.add_to_current_key("services_status","language",0)

        match language_status["language"]:
            case 0:
                self.ui.language_start_pushButton.setText("Stop")
                self.dashboard_session.add_to_current_key("services_status", "language", 1)
            case 1:
                self.ui.language_start_pushButton.setText("Start")
                self.dashboard_session.add_to_current_key("services_status", "language", 0)

        data_to_save = {
            "service": "language",
            "type": self.ui.language_type_label.text(),
            "version": self.ui.language_version_label.text(),
            "is_running": language_status["language"],
        }
        self.dashboard_service.update_language_info(data_to_save)

    def switch_state_network(self):
        print("Chạy độc lập loại network nào đó ví dụ ngrok hoặc telnet")

    def listener_webserver_saved(self,data):
        webserver_status = self.dashboard_session.get("services_status")
        self.ui.webserver_type_label.setText(data["server_name"])
        self.ui.webserver_version_label.setText(data["selected_version"])
        data["is_running"] = webserver_status["webserver"]
        self.dashboard_service.update_webserver_info(data)

    def listener_database_saved(self,data):
        database_status = self.dashboard_session.get("services_status")
        status = database_status["database"] if "database" in database_status else 0
        self.ui.database_type_label.setText(data["type"])
        self.ui.database_version_label.setText(data["root_path"])
        data["is_running"] = status
        data["service"] = "database"
        self.dashboard_service.update_database_info(data)

    def listener_language_saved(self,data):
        language_status = self.dashboard_session.get("services_status")
        status = language_status["language"] if "language" in language_status else 0
        self.ui.language_type_label.setText(data["language"])
        self.ui.language_version_label.setText(data["selected_version"])
        data["is_running"] = status
        self.dashboard_service.update_language_info(data)

    def listener_tool_saved(self,data: dict):
        print(f"thông tin từ tool: {data}")

    def listener_network_saved(self,data):
        print("nhận emit từ network rồi lưu thông tin")


    def handle_on_log_received(self, data):
        logger.info(data)

    def handle_on_status_changed(self, data):
        logger.info(data)