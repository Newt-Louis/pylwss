from PySide6.QtWidgets import QWidget
from ui.windows.origin_interface import Ui_ToolsPage
from ui.widgets.CollapsibleItem import CollapsibleItem


class ToolsPageController(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model

        self.ui = Ui_ToolsPage()

        self.ui.setupUi(self)

    def on_save_changes(self):
        print("Lưu cấu hình redis...")

    def on_redis_selected(self, checked):
        if checked:
            print("Redis đang được bật.")
