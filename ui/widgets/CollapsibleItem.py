from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QCheckBox, QFrame
)
from PySide6.QtCore import Qt, QEasingCurve, QPropertyAnimation, QRect

class CollapsibleItem(QWidget):
    def __init__(self, title="Untitled", uid=None,parent=None):
        super().__init__(parent)
        if not uid:
            raise ValueError("Tham số 'uid' là bắt buộc để định danh CollapsibleItem và CheckBox bên trong.")
        self.uid = uid

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.header = QWidget()
        self.headerLayout = QHBoxLayout(self.header)
        self.headerLayout.setContentsMargins(8, 4, 8, 4)

        self.toggleBtn = QPushButton("▶")
        self.toggleBtn.setFlat(True)
        self.toggleBtn.setFixedWidth(25)
        self.toggleBtn.setFocusPolicy(Qt.NoFocus)
        self.toggleBtn.clicked.connect(self.toggle)

        self.titleLabel = QLabel(title)
        self.titleLabel.setStyleSheet("font-weight: 700; font-size: 14px;")

        self.checkBox = QCheckBox()
        self.checkBox.setObjectName(f"{uid}_checkBox")
        self.checkBox.setStyleSheet(self._checkbox_custom_style())

        self.headerLayout.addWidget(self.toggleBtn)
        self.headerLayout.addWidget(self.titleLabel)
        self.headerLayout.addStretch()
        self.headerLayout.addWidget(self.checkBox)

        self.header.mousePressEvent = self._headerClicked

        self.mainLayout.addWidget(self.header)

        self.content = QWidget()
        self.content.setMaximumHeight(0)  # bắt đầu ẩn
        self.content.setVisible(False)
        self.contentLayout = QGridLayout(self.content)
        self.contentLayout.setContentsMargins(30, 4, 8, 4)

        self.mainLayout.addWidget(self.content)

        self.anim = QPropertyAnimation(self.content, b"maximumHeight")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.finished.connect(self._on_animation_finished)

    def _headerClicked(self, event):
        # Nếu click lên checkbox thì không toggle
        if self.checkBox.geometry().contains(event.position().toPoint()):
            return
        # Còn lại thì toggle
        self.toggle()

    def toggle(self):
        opening = not self.content.isVisible()

        # Đổi icon mũi tên
        self.toggleBtn.setText("▼" if opening else "▶")

        if opening:
            self.content.setVisible(True)
            self._animate_open()
        else:
            self._animate_close()

    def _animate_open(self):
        self.content.setMaximumHeight(0)
        self.anim.stop()
        target_height = self.content.sizeHint().height()
        self.anim.setStartValue(0)
        self.anim.setEndValue(target_height)
        self.anim.start()

    def _animate_close(self):
        start_height = self.content.height()
        self.anim.stop()
        self.anim.setStartValue(start_height)
        self.anim.setEndValue(0)
        self.anim.start()

    def _on_animation_finished(self):
        if self.anim.endValue() == 0:
            self.content.setVisible(False)

    def _checkbox_custom_style(self):
        tick_icon_url = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAYklEQVR42mNgGRjwm4Hhf4L4P5D+jw0DA1Ea/jMw/IeJ/kfW9B+I/wPxfaQYgGw4sh50O0D4P1IMAnoc2Q0w/o/E/5FieMCRg/B/pBgEdDiyHmQ7/iPFIKDDkfWg2wHC/5FiEAAA1i48q/c+25gAAAAASUVORK5CYII="

        return f"""
            QCheckBox {{
                spacing: 5px;
                font-size: 14px;
            }}
            /* Phần ô vuông (Indicator) */
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border-radius: 4px; /* Bo tròn nhẹ */
                border: 1px solid #999; /* Viền xám mặc định */
                background-color: #f0f0f0; /* Nền xám nhạt */
            }}

            /* Khi di chuột vào (Hover) */
            QCheckBox::indicator:hover {{
                border: 1px solid #0078d7; /* Viền xanh */
                background-color: #ffffff;
            }}

            /* Khi đã tick (Checked) */
            QCheckBox::indicator:checked {{
                background-color: #0078d7; /* Nền xanh chuẩn Windows */
                border: 1px solid #0078d7;
                image: url(:/icons/white_check.png);
            }}

            /* Khi đã tick nhưng di chuột vào */
            QCheckBox::indicator:checked:hover {{
                background-color: #0063b1; /* Xanh đậm hơn chút */
                border: 1px solid #0063b1;
            }}

            /* Khi bị disable*/
            QCheckBox::indicator:disabled {{
                background-color: #e0e0e0;
                border: 1px solid #ccc;
            }}
        """

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QCheckBox, QLineEdit

    app = QApplication(sys.argv)

    w = QWidget()
    layout = QVBoxLayout(w)

    item = CollapsibleItem("Utility: Network Scanner","network")
    item.contentLayout.addWidget(QCheckBox("Enable IPv6"),0,0)
    item.contentLayout.addWidget(QLineEdit("Range: 192.168.1.1/24"),0,1)

    item2 = CollapsibleItem("Utility: File Cleaner","file_cleaner")
    item2.contentLayout.addWidget(QCheckBox("Include Temp Folder"),0,0)
    item2.contentLayout.addWidget(QCheckBox("Ask before deleting"),0,1)

    layout.addWidget(item)
    layout.addWidget(item2)

    layout.addStretch()

    w.resize(400, 400)
    w.show()
    sys.exit(app.exec())
