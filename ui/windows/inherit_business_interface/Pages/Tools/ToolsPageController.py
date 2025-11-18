from PySide6.QtWidgets import QWidget,QVBoxLayout,QFileDialog,QLabel,QLineEdit,QPushButton,QMessageBox

from .ToolsServiceController import ToolsServiceController
from ui.windows.origin_interface import Ui_ToolsPage
from ui.widgets.RedisCollapsible import RedisCollapsible


class ToolsPageController(QWidget):
    def __init__(self, model=None):
        super().__init__()
        self.model = model
        self.ui = Ui_ToolsPage()
        self.ui.setupUi(self)
        self.tools_service_controller = ToolsServiceController()
        if self.ui.content_area.layout() is None:
            self.ui.content_area.setLayout(QVBoxLayout())
        self.redis_item = RedisCollapsible()
        self.ui.content_area.layout().addWidget(self.redis_item)
        self.ui.tools_save_buttonBox.accepted.connect(self.on_save_changes)

    def on_save_changes(self):
        redis_info = self.redis_item.get_config()
        if not redis_info["path"] or redis_info["path"] is None:
            QMessageBox.critical(self, "Info missing", "Redis need root path")
            return
        try:
            result = self.tools_service_controller.on_save_changes(redis=redis_info)
            if result:
                QMessageBox.information(self, "Info saved", "Save tools config successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
