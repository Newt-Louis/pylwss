from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QFileDialog
)
from ui.widgets.CollapsibleItem import CollapsibleItem


class RedisCollapsible(CollapsibleItem):
    def __init__(self, parent=None):
        super().__init__("Redis", "redis_collapsible", parent)

        self.lbl_port = QLabel("Port:")

        self.port_edit = QLineEdit()
        self.port_edit.setObjectName("redis_port_lineEdit")
        self.port_edit.setPlaceholderText("VD: 6379")

        self.lbl_path = QLabel("Redis Path:")

        self.path_edit = QLineEdit()
        self.path_edit.setObjectName("redis_path_lineEdit")
        self.path_edit.setPlaceholderText("Chọn thư mục Redis portable...")

        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.on_browse_path)

        self.contentLayout.addWidget(self.lbl_port, 0, 0)
        self.contentLayout.addWidget(self.port_edit, 0, 1)

        self.contentLayout.addWidget(self.lbl_path, 1, 0)
        self.contentLayout.addWidget(self.path_edit, 1, 1)
        self.contentLayout.addWidget(self.browse_btn, 1, 2)

        self.checkBox.toggled.connect(self.on_redis_checked)

    def on_browse_path(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Chọn thư mục Redis portable",
            "",
        )
        if folder:
            self.path_edit.setText(folder)

    def on_redis_checked(self, checked):
        if checked:
            print("Redis đang được bật.")
        else:
            print("Redis đã tắt.")

    def get_config(self):
        return {
            "is_chosen": self.checkBox.isChecked(),
            "port": self.port_edit.text(),
            "root_path": self.path_edit.text(),
        }
