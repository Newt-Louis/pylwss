from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
from pathlib import Path
from PySide6.QtWidgets import QWidget, QMessageBox
from ui.windows.origin_interface import Ui_DatabasesPage
from .DatabasesServiceController import DatabasesServiceController

class DatabasesPageController(QWidget):
    BROWSE_MAP={}
    DATABASES_GROUP=[
        "radio",
        "port_lineEdit",
        "service_dir_lineEdit",
        "service_dir_browseButton",
        "data_dir_lineEdit",
        "data_dir_browseButton",
        "config_pushButton"
    ]
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.ui = Ui_DatabasesPage()
        self.ui.setupUi(self)
        self.service_controller = DatabasesServiceController()

        ini_database_settings = self.service_controller.load_data()
        if ini_database_settings:
            self.on_load_init_data(ini_database_settings)
        else:
            print("Hiển thị sẵn 1 vài ví dụ cấu hình gì đó lên trang Databases")

        self.ui.database_save_change_buttonBox.clicked.connect(self.on_save_changes)
        self.ui.mysql_radio.toggled.connect(self.on_mysql_selected)

    def on_save_changes(self):
        print("Lưu cấu hình databases...")
        # Lấy dữ liệu từ self.ui.mysql_version_combobox.currentText()
        # và gọi self.model.save_config(...)

    def on_mysql_selected(self, checked):
        if checked:
            print("MySQL được chọn.")

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

    def open_user_ini(self,settings:dict):
        file_path = Path(settings["root_path"]) / "user.ini"
        if file_path.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(file_path)))
        else:
            QMessageBox.warning(self, "File not found", f"Không tìm thấy file:\n{file_path}")