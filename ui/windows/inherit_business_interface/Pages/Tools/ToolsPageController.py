from PySide6.QtWidgets import QWidget,QVBoxLayout,QFileDialog,QLabel,QLineEdit,QPushButton,QMessageBox
from ui.windows.origin_interface import Ui_ToolsPage
from ui.widgets.CollapsibleItem import CollapsibleItem


class ToolsPageController(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.ui = Ui_ToolsPage()
        self.ui.setupUi(self)
        if self.ui.content_area.layout() is None:
            self.ui.content_area.setLayout(QVBoxLayout())
        self.collapse_items = {
            "redis": self.create_redis_item()
        }
        self.ui.content_area.layout().addWidget(self.collapse_items["redis"])


    def on_save_changes(self):
        port = self.collapse_items["redis"].redis_port_lineEdit.text()
        path = self.collapse_items["redis"].redis_path_lineEdit.text()
        enabled = self.redis_item.checkBox.isChecked()

        print("Lưu cấu hình Redis...")
        print("  Enabled:", enabled)
        print("  Port:", port)
        print("  Path:", path)

    def on_redis_selected(self, checked):
        if checked:
            print("Redis đang được bật.")

    def create_redis_item(self):
        item = CollapsibleItem("Redis Service")

        lbl_port = QLabel("Port:")
        redis_port_edit = QLineEdit()
        redis_port_edit.setObjectName("redis_port_lineEdit")
        redis_port_edit.setPlaceholderText("VD: 6379")

        lbl_path = QLabel("Redis Path:")
        redis_path_edit = QLineEdit()
        redis_path_edit.setObjectName("redis_path_lineEdit")
        redis_path_edit.setPlaceholderText("Chọn thư mục Redis portable...")

        redis_browse_btn = QPushButton("Browse")
        redis_browse_btn.clicked.connect(self.on_browse_redis_path)

        item.contentLayout.addWidget(lbl_port, 0, 0)
        item.contentLayout.addWidget(redis_port_edit, 0, 1)

        item.contentLayout.addWidget(lbl_path, 1, 0)
        item.contentLayout.addWidget(redis_path_edit, 1, 1)
        item.contentLayout.addWidget(redis_browse_btn, 1, 2)

        item.checkBox.stateChanged.connect(self.on_redis_selected)

        return item

    # ================================================================
    # Click Browse → mở FolderDialog → gán vào lineEdit redis_path_edit
    # ================================================================
    def on_browse_redis_path(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Chọn thư mục Redis portable",
            "",
        )
        if folder:
            self.redis_path_edit.setText(folder)

    # ================================================================
    # Xử lý khi bật/tắt Redis checkbox
    # ================================================================
    def on_redis_selected(self, checked):
        if checked:
            print("Redis đang được bật.")
        else:
            print("Redis đã tắt.")