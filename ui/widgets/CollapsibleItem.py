from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QCheckBox, QSizePolicy
)
from PySide6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QRect


class CollapsibleItem(QWidget):
    def __init__(self, title="Untitled", parent=None):
        super().__init__(parent)

        # ============ MAIN LAYOUT ============
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # ============ HEADER ============
        self.header = QWidget()
        self.headerLayout = QHBoxLayout(self.header)
        self.headerLayout.setContentsMargins(8, 4, 8, 4)

        # Toggle button (mũi tên)
        self.toggleBtn = QPushButton("▶")
        self.toggleBtn.setFlat(True)
        self.toggleBtn.setFixedWidth(25)
        self.toggleBtn.setFocusPolicy(Qt.NoFocus)
        self.toggleBtn.clicked.connect(self.toggle)

        # Title label
        self.titleLabel = QLabel(title)
        self.titleLabel.setStyleSheet("font-weight: 500;")

        # Checkbox bên phải
        self.checkBox = QCheckBox()
        self.checkBox.setObjectName("$$_checkBox")

        # Layout header
        self.headerLayout.addWidget(self.toggleBtn)
        self.headerLayout.addWidget(self.titleLabel)
        self.headerLayout.addStretch()
        self.headerLayout.addWidget(self.checkBox)

        # Click cả header để toggle
        self.header.mousePressEvent = self._headerClicked

        # Add header to layout
        self.mainLayout.addWidget(self.header)

        # ============ CONTENT AREA ============
        self.content = QWidget()
        self.content.setMaximumHeight(0)  # bắt đầu ẩn
        self.content.setVisible(False)
        self.contentLayout = QGridLayout(self.content)
        self.contentLayout.setContentsMargins(30, 4, 8, 4)

        self.mainLayout.addWidget(self.content)

        # Animation cho mượt
        self.anim = QPropertyAnimation(self.content, b"maximumHeight")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)

    # ============================================================
    # Toggle header click
    # ============================================================
    def _headerClicked(self, event):
        # Nếu click lên checkbox thì không toggle
        if self.checkBox.geometry().contains(event.position().toPoint()):
            return
        # Còn lại thì toggle
        self.toggle()

    # ============================================================
    # Toggle expand/collapse
    # ============================================================
    def toggle(self):
        opening = not self.content.isVisible()

        # Đổi icon mũi tên
        self.toggleBtn.setText("▼" if opening else "▶")

        if opening:
            self.content.setVisible(True)
            self._animate_open()
        else:
            self._animate_close()

    # ============================================================
    # Animation mở
    # ============================================================
    def _animate_open(self):
        self.content.setMaximumHeight(0)
        self.anim.stop()
        target_height = self.content.sizeHint().height()
        self.anim.setStartValue(0)
        self.anim.setEndValue(target_height)
        self.anim.start()

    # ============================================================
    # Animation đóng
    # ============================================================
    def _animate_close(self):
        start_height = self.content.height()
        self.anim.stop()
        self.anim.setStartValue(start_height)
        self.anim.setEndValue(0)
        self.anim.start()
        self.anim.finished.connect(lambda: self.content.setVisible(False))


# =================================================================
# DEMO CHẠY NGAY TRONG FILE (không ảnh hưởng project chính)
# =================================================================
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QCheckBox, QLineEdit

    app = QApplication(sys.argv)

    w = QWidget()
    layout = QVBoxLayout(w)

    item = CollapsibleItem("Utility: Network Scanner")
    item.contentLayout.addWidget(QCheckBox("Enable IPv6"),0,0)
    item.contentLayout.addWidget(QLineEdit("Range: 192.168.1.1/24"),0,1)

    item2 = CollapsibleItem("Utility: File Cleaner")
    item2.contentLayout.addWidget(QCheckBox("Include Temp Folder"),0,0)
    item2.contentLayout.addWidget(QCheckBox("Ask before deleting"),0,1)

    layout.addWidget(item)
    layout.addWidget(item2)

    layout.addStretch()

    w.resize(400, 400)
    w.show()
    sys.exit(app.exec())
