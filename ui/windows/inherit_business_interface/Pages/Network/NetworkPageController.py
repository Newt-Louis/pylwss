from PySide6.QtWidgets import QWidget
# 1. Import lớp giao diện đã được build từ file .py
from ui.windows.origin_interface import Ui_NetworkPage


class NetworkPageController(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model

        # 2. Khởi tạo một đối tượng từ lớp giao diện
        self.ui = Ui_NetworkPage()

        # 3. Dùng phương thức setupUi() để vẽ giao diện lên chính widget controller này (self)
        self.ui.setupUi(self)

        # 4. Từ đây, mọi thứ giống hệt như trước!
        # Kết nối signals và slots như bình thường.
        # IDE của bạn bây giờ sẽ gợi ý code khi bạn gõ self.ui. ...
        self.ui.network_save_change_buttonbox.accepted.connect(self.on_save_changes)
        self.ui.telnet_checkbox.toggled.connect(self.on_telnet_selected)

    def on_save_changes(self):
        print("Lưu cấu hình telnet...")

    def on_telnet_selected(self, checked):
        if checked:
            print("Telnet được chọn.")
