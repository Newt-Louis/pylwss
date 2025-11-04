from PySide6.QtWidgets import QWidget
from ui.windows.origin_interface import Ui_DatabasesPage


class DatabasesPageController(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.ui = Ui_DatabasesPage()
        self.ui.setupUi(self)

        # TODO: Kiểm tra thông tin trong bảng database_settings và thực hiện download giải nén
        # cùng cấu hình các thông tin ban đầu cho mysql ngay sau khi ứng dụng được cài đặt xong
        # sau khi đã có mysql trong ứng dụng rồi thì lưu các thông tin ban đầu vào database
        # và cho phép hoạt động lại như bình thường

        self.ui.database_save_change_buttonbox.clicked.connect(self.on_save_changes)
        self.ui.mysql_radio.toggled.connect(self.on_mysql_selected)

    def on_save_changes(self):
        print("Lưu cấu hình databases...")
        # Lấy dữ liệu từ self.ui.mysql_version_combobox.currentText()
        # và gọi self.model.save_config(...)

    def on_mysql_selected(self, checked):
        if checked:
            print("MySQL được chọn.")
