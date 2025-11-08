import os
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from pathlib import Path
from PySide6.QtWidgets import QWidget, QMessageBox, QFileDialog

from core.manager.DashboardSession import DashboardSession
from ui.windows.origin_interface import Ui_DatabasesPage
from .DatabasesServiceController import DatabasesServiceController

class DatabasesPageController(QWidget):
    BROWSE_MAP={
        "mysql_service_dir_browseButton":("folder","mysql_service_dir_lineEdit"),
        "mysql_data_dir_browseButton":("folder","mysql_data_dir_lineEdit"),
        "mariadb_service_dir_browseButton":("folder","mariadb_service_dir_lineEdit"),
        "mariadb_data_dir_browseButton":("folder","mariadb_data_dir_lineEdit"),
        "postgresql_service_dir_browseButton":("folder","postgresql_service_dir_lineEdit"),
        "postgresql_data_dir_browseButton":("folder","postgresql_data_dir_lineEdit"),
        "mongodb_service_dir_browseButton":("folder","mongodb_service_dir_lineEdit"),
        "mongodb_data_dir_browseButton":("folder","mongodb_data_dir_lineEdit"),
    }
    DATABASES_GROUP={
        "mysql":[
            "mysql_port_lineEdit",
            "mysql_service_dir_lineEdit",
            "mysql_service_dir_browseButton",
            "mysql_data_dir_lineEdit",
            "mysql_data_dir_browseButton",
            "mysql_config_pushButton"
        ],
        "mariadb":[
            "mariadb_port_lineEdit",
            "mariadb_service_dir_lineEdit",
            "mariadb_service_dir_browseButton",
            "mariadb_data_dir_lineEdit",
            "mariadb_data_dir_browseButton",
            "mariadb_config_pushButton"
        ],
        "postgresql":[
            "postgresql_port_lineEdit",
            "postgresql_service_dir_lineEdit",
            "postgresql_service_dir_browseButton",
            "postgresql_data_dir_lineEdit",
            "postgresql_data_dir_browseButton",
            "postgresql_config_pushButton"
        ],
        "mongodb":[
            "mongodb_port_lineEdit",
            "mongodb_service_dir_lineEdit",
            "mongodb_service_dir_browseButton",
            "mongodb_data_dir_lineEdit",
            "mongodb_data_dir_browseButton",
            "mongodb_config_pushButton"
        ],
    }
    CONFIG_BUTTON = ["mysql_config_pushButton","mariadb_config_pushButton","postgresql_config_pushButton","mongodb_config_pushButton"]
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.ui = Ui_DatabasesPage()
        self.ui.setupUi(self)
        self.service_controller = DatabasesServiceController()
        self.dashboard_session = DashboardSession()
        for config_button in self.CONFIG_BUTTON:
            button = getattr(self.ui, f"{config_button}")
            button.setEnabled(False)

        ini_database_settings = self.service_controller.load_data()
        if ini_database_settings:
            self.on_load_init_data(ini_database_settings)
        else:
            QMessageBox.information(self,"Database Infomation Empty","Ứng dụng khởi động lần đầu, cần chọn loại database và thêm thông tin cấu hình")

        for button_name in DatabasesPageController.BROWSE_MAP.keys():
            try:
                button_widget = getattr(self.ui, button_name)
                button_widget.clicked.connect(self.on_browse_button_clicked)
            except AttributeError:
                print(f"Lỗi: Không tìm thấy nút browse trong UI: {button_name}")

        self.ui.database_save_change_buttonBox.clicked.connect(self.on_save_changes)
        self.ui.mysql_radio.toggled.connect(lambda: self.on_database_selected("mysql"))
        self.ui.mariadb_radio.toggled.connect(lambda: self.on_database_selected("mariadb"))
        self.ui.postgresql_radio.toggled.connect(lambda: self.on_database_selected("postgresql"))
        self.ui.mongodb_radio.toggled.connect(lambda: self.on_database_selected("mongodb"))

    def on_save_changes(self):
        current_database_selected = self.dashboard_session.get("database_page_selected")
        port = getattr(self.ui, f"{current_database_selected}_port_lineEdit").text()
        service_dir = getattr(self.ui, f"{current_database_selected}_service_dir_lineEdit").text()
        data_dir = getattr(self.ui, f"{current_database_selected}_data_dir_lineEdit").text()
        selected = getattr(self.ui, f"{current_database_selected}_radio").isChecked()

        port = port if port.strip() else None
        root_path = service_dir if service_dir.strip() else None
        data_dir = data_dir if data_dir.strip() else None
        setting_dict = {
            "type": current_database_selected,
            "port": port,
            "root_path": root_path,
            "base_data_path": data_dir,
            "is_chosen": selected,
        }
        required_fileds = {
            "type": "Type",
            "port": "Port",
            "root_path": "Service Directory",
            "base_data_path": "Data Directory",
        }
        for field_key, field_name in required_fileds.items():
            if not setting_dict[field_key]:
                QMessageBox.warning(self, "Thiếu thông tin", f"'{field_name}' không được trống!")
                return
        result = self.service_controller.save_changes(setting_dict)
        QMessageBox.information(self, "Thành công", "Đã lưu tất cả thay đổi!") \
            if result else QMessageBox.critical(self, "Lỗi", "Có lỗi xảy ra trong quá trình lưu cấu hình!")

    def on_database_selected(self, database:str):
        for str_database, widgets in DatabasesPageController.DATABASES_GROUP.items():
            enabled = str_database == database
            for str_widget in widgets:
                widget = getattr(self.ui, str_widget)
                widget.setEnabled(enabled)

            if enabled:
                config_button = getattr(self.ui, f"{database}_config_pushButton")
                service_dir_widget = getattr(self.ui, f"{database}_service_dir_lineEdit")
                service_dir = service_dir_widget.text()
                if service_dir:
                    config_button.setEnabled(enabled)
                    config_button.clicked.connect(lambda: self.open_config_file(service_dir))
                else:
                    config_button.setEnabled(False)
        self.dashboard_session.set("database_page_selected", database)

    def on_load_init_data(self,settings:list[dict]):
        for setting in settings:
            db_type = setting["type"]  # ví dụ: "mysql", "mariadb", "postgresql", ...
            widgets = {
                "radio": getattr(self.ui, f"{db_type}_radio", None),
                "port": getattr(self.ui, f"{db_type}_port_lineEdit", None),
                "service_dir": getattr(self.ui, f"{db_type}_service_dir_lineEdit", None),
                "data_dir": getattr(self.ui, f"{db_type}_data_dir_lineEdit", None),
            }
            widgets["radio"].setChecked(setting.get("is_chosen", False))
            widgets["port"].setText(str(setting.get("port", "")))
            widgets["service_dir"].setText(setting.get("root_path", ""))
            widgets["data_dir"].setText(setting.get("base_data_path", ""))
            config_button = getattr(self.ui, f"{db_type}_config_pushButton", None)
            if setting["root_path"] and setting["is_chosen"]:
                config_button.setEnabled(setting["is_chosen"])
                config_button.clicked.connect(lambda: self.open_config_file(db_type,setting["root_path"]))
                self.dashboard_session.set("database_page_selected", db_type)
            else:
                config_button.setEnbabled(setting["is_chosen"])

    def open_config_file(self,database:str,root_path:str):
        ini_files = {
            "mysql": "user.ini",
            "mariadb": "user.ini",
            "postgresql": "postgresql.conf",
            "mongodb": "mongod.conf",
        }
        filename = ini_files.get(database, "user.ini")
        file_path = Path(root_path) / filename
        if file_path.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(file_path)))
        else:
            QMessageBox.warning(self, "File not found", f"Không tìm thấy file:\n{file_path}")

    def on_browse_button_clicked(self):
        sender_button_name = self.sender().objectName()
        if sender_button_name not in DatabasesPageController.BROWSE_MAP:
            QMessageBox.warning(self, "Lỗi", f"Không tìm thấy cấu hình browse cho: {sender_button_name}")
            return

        config = DatabasesPageController.BROWSE_MAP[sender_button_name]
        dialog_type, target_line_edit_name = config[:2]
        target_line_edit = getattr(self.ui, target_line_edit_name)

        current_path = target_line_edit.text()
        if not os.path.isdir(current_path):  # Kiểm tra xem đường dẫn có hợp lệ không
            current_path = "C:/"  # Mặc định

        selected_path = ""

        if dialog_type == "folder":
            selected_path = QFileDialog.getExistingDirectory(
                self,
                "Chọn thư mục gốc",  # Tiêu đề cửa sổ
                current_path  # Thư mục bắt đầu
            )
        elif dialog_type == "file":
            file_filter = config[2] if len(config) > 2 else "All Files (*)"
            selected_path, _ = QFileDialog.getOpenFileName(
                self,
                "Chọn tệp tin",
                current_path,
                file_filter
            )

        if selected_path:
            normalized_path = os.path.normpath(selected_path)
            target_line_edit.setText(normalized_path)