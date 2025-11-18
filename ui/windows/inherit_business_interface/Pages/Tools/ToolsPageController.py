from PySide6.QtWidgets import QWidget,QVBoxLayout,QFileDialog,QLabel,QLineEdit,QPushButton,QMessageBox
from ui.windows.origin_interface import Ui_ToolsPage
from ui.widgets.RedisCollapsible import RedisCollapsible


class ToolsPageController(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.ui = Ui_ToolsPage()
        self.ui.setupUi(self)
        if self.ui.content_area.layout() is None:
            self.ui.content_area.setLayout(QVBoxLayout())
        self.redis_item = RedisCollapsible()
        self.ui.content_area.layout().addWidget(self.redis_item)


    def on_save_changes(self):
        redis_info = self.redis_item.get_config()

        print("Lưu cấu hình Redis:", redis_info)