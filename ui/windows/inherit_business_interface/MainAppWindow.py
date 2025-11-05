from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, QByteArray
from ui.windows.origin_interface import Ui_MainWindow
from ui.windows.inherit_business_interface import DatabasesPageController
from ui.windows.inherit_business_interface import DashboardPageController
from ui.windows.inherit_business_interface import LanguagesPageController
from ui.windows.inherit_business_interface import WebserverPageController
from ui.windows.inherit_business_interface import NetworkPageController
from ui.windows.inherit_business_interface import ToolsPageController

class MainAppWindow(QMainWindow):
    def __init__(self):
        # Gọi hàm khởi tạo của lớp cha (QMainWindow)
        super().__init__()
        # self.core_model = AppModel()
        # Tạo một đối tượng từ class giao diện
        self.ui = Ui_MainWindow()
        # Dùng phương thức setupUi để vẽ giao diện lên cửa sổ chính (self)
        self.ui.setupUi(self)

        # Lưu lại trạng thái của sidebar (True = đang mở)
        self.is_sidebar_visible = True
        # Kích thước ban đầu
        self.sidebar_original_width = 0
        self.apply_button_styles()
        self.ui.toggle_sidebar_button.clicked.connect(self.toggle_sidebar)

        # Đặt tiêu đề cho cửa sổ
        self.setWindowTitle("PyLWSSM")

        # Gọi phương thức để kết nối các tín hiệu (signals) và hành động (slots)
        self._setup_navigation()

    def _setup_navigation(self):
        """
        Thiết lập các trang và kết nối các nút bấm sidebar một cách tự động.
        """
        self.pages_config = [
            (self.ui.dashboard_button, DashboardPageController),
            (self.ui.languages_button, LanguagesPageController),
            (self.ui.databases_button, DatabasesPageController),
            (self.ui.webserver_button, WebserverPageController),
            (self.ui.tools_button, ToolsPageController),
            (self.ui.network_button, NetworkPageController),
        ]

        for button, PageControllerClass in self.pages_config:
            page = PageControllerClass(None)
            self.ui.main_content_area.addWidget(page)
            # Kết nối tín hiệu được thực hiện ngay tại đây!
            button.clicked.connect(lambda checked=False, page=page: self.ui.main_content_area.setCurrentWidget(page))

        # Thiết lập trang mặc định
        if self.pages_config:
            self.pages_config[0][0].setChecked(True)
            default_page = self.ui.main_content_area.widget(0)
            self.ui.main_content_area.setCurrentWidget(default_page)

    def apply_button_styles(self):
        """Áp dụng QSS để tạo hiệu ứng cho nút."""
        style = """
            QToolButton#toggle_sidebar_button {
                border: none;
                background-color: transparent;
                padding: 5px;
            }

            /* Hiệu ứng khi di chuột vào (hover) */
            QToolButton#toggle_sidebar_button:hover {
                background-color: #bebebe; /* Hơi xám để nổi bật */
                border-radius: 5px;
            }

            /* Hiệu ứng khi nhấn chuột xuống (pressed) */
            QToolButton#toggle_sidebar_button:pressed {
                background-color: #dcdcdc; /* Xám đậm hơn để giả lập hiệu ứng nhấn */
                padding-left: 7px; /* Di chuyển icon sang phải một chút */
                padding-top: 7px;  /* Di chuyển icon xuống một chút */
            }
        """
        self.ui.toggle_sidebar_button.setStyleSheet(style)

    def toggle_sidebar(self):
        """Hàm xử lý việc ẩn/hiện sidebar."""
        sidebar = self.ui.main_left_sidebar_layout
        start_width = sidebar.width()

        # Kiểm tra xem sidebar có đang hiển thị không
        if self.is_sidebar_visible:
            end_width = 50
            self.is_sidebar_visible = False
        else:
            end_width = self.sidebar_original_width
            self.is_sidebar_visible = True

        # Tạo animation
        # QPropertyAnimation(target, propertyName)
        self.animation = QPropertyAnimation(sidebar, QByteArray(b"maximumWidth"))
        self.animation.setDuration(300)  # Thời gian animation (300ms)
        self.animation.setStartValue(start_width)
        self.animation.setEndValue(end_width)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuart)  # Kiểu animation
        self.animation.start()

    def showEvent(self, event, /):
        if self.sidebar_original_width == 0:
            self.sidebar_original_width = self.ui.main_left_sidebar_layout.width()
            super().showEvent(event)