import os
from PySide6.QtWidgets import QWidget, QRadioButton, QFileDialog, QMessageBox
from core.manager.DashboardSession import DashboardSession
from ui.windows.origin_interface import Ui_LanguagesPage
from .LanguagesServiceController import LanguagesServiceController


class LanguagesPageController(QWidget):
    BROWSE_MAP = {
        "php_browse_root_folder_pushbutton":("folder","php_root_folder_lineedit"),
        "python_browse_root_folder_pushbutton":("folder","python_root_folder_lineedit"),
        "java_browse_root_folder_pushbutton":("folder","java_root_folder_lineedit"),
        "nodejs_browse_root_folder_pushbutton":("folder","nodejs_root_folder_lineedit"),
    }
    LANGUAGE_GROUP = {
        "php": [
            "php_combobox",
            "php_ssl_enabled_checkbox",
            "php_port_lineedit",
            "php_root_folder_lineedit",
            "php_browse_root_folder_pushbutton",
        ],
        "python": [
            "python_combobox",
            "python_ssl_enabled_checkbox",
            "python_port_lineedit",
            "python_root_folder_lineedit",
            "python_browse_root_folder_pushbutton",
        ],
        "java": [
            "java_combobox",
            "java_ssl_enabled_checkbox",
            "java_port_lineedit",
            "java_root_folder_lineedit",
            "java_browse_root_folder_pushbutton",
        ],
        "nodejs": [
            "nodejs_combobox",
            "nodejs_ssl_enabled_checkbox",
            "nodejs_port_lineedit",
            "nodejs_root_folder_lineedit",
            "nodejs_browse_root_folder_pushbutton",
        ],
    }
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.ui = Ui_LanguagesPage()
        self.ui.setupUi(self)
        self.language_core_service = LanguagesServiceController()
        self.dashboard_session = DashboardSession()

        self.setStyleSheet("""
                    /* --- Trạng thái CHƯA CHECK --- */
                    QCheckBox::indicator:unchecked {
                        background-color: #FFFFFF;
                        border: 1px solid #767676; /* Viền xám */
                    }
                    /* Khi di chuột vào (chưa check) */
                    QCheckBox::indicator:unchecked:hover {
                        border: 1px solid #000000;
                    }

                    /* --- Trạng thái ĐÃ CHECK (Quan trọng nhất) --- */
                    QCheckBox::indicator:checked {
                        background-color: #0078D7;
                        border: 1px solid #000000;
                    }
                    /* Khi di chuột vào (đã check) */
                    QCheckBox::indicator:checked:hover {
                        background-color: #005A9E; /* Nền xanh đậm hơn */
                        border: 1px solid #005A9E;
                    }
                """)

        # Chạy các hàm khởi tạo hoặc lấy dữ liệu ban đầu
        try:
            # Phiên bản cho hộp combobox
            languages_version_data = self.language_core_service.load_languages_version()
            if languages_version_data is None:
                QMessageBox.warning(self, "Cảnh báo", "Dữ liệu trong database đang rỗng!")
            else:
                for key, row in languages_version_data.items():
                    combobox = getattr(self.ui,f"{key}_combobox")
                    combobox.addItems([sqlite_row["version"] for sqlite_row in row])
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Database versions có lỗi {str(e)}")
        try:
            # Cấu hình ngôn ngữ đang được chọn
            languages_init_data = self.language_core_service.load_data()
            if languages_init_data is None:
                QMessageBox.warning(self,"Cảnh báo","Dữ liệu trong database đang rỗng!")
            else:
                chosen_language = None
                for language_setting in languages_init_data:
                    self.init_settings_data(language_setting.language, language_setting)
                    if language_setting.is_chosen:
                        chosen_language = language_setting.language

                if chosen_language:
                    radio_button = getattr(self.ui, f"{chosen_language}_radio")
                    radio_button.setChecked(True)
                    self.on_language_selected(chosen_language)
                else: self.on_language_selected("")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Database settings có lỗi: {str(e)}")

        # Gán sự kiện cho các nút
        self.ui.language_save_change_buttonbox.accepted.connect(self.on_save_changes)
        self.ui.php_radio.clicked.connect(lambda checked: self.on_language_selected("php"))
        self.ui.python_radio.clicked.connect(lambda checked: self.on_language_selected("python"))
        self.ui.java_radio.clicked.connect(lambda checked: self.on_language_selected("java"))
        self.ui.nodejs_radio.clicked.connect(lambda checked: self.on_language_selected("nodejs"))

        for lang in self.LANGUAGE_GROUP.keys():
            try:
                ssl_checkbox = getattr(self.ui, f"{lang}_ssl_enabled_checkbox")
                ssl_checkbox.toggled.connect(
                    lambda checked, l=lang: self._set_ssl_checkbox_toggled(l, checked)
                )
            except AttributeError as e:
                print(f"Lỗi: Không tìm thấy {lang}_ssl_enabled_checkbox: {e}")

        for button_name in self.BROWSE_MAP.keys():
            try:
                button_widget = getattr(self.ui, button_name)
                button_widget.clicked.connect(self.on_browse_button_clicked)
            except AttributeError:
                print(f"Lỗi: Không tìm thấy nút browse trong UI: {button_name}")

    def on_save_changes(self):
        current_language_selected = self.dashboard_session.get("language_page_selected")
        try:
            # 1. Lấy các giá trị mới từ UI
            selected_version = getattr(self.ui, f"{current_language_selected}_combobox").currentText()
            root_folder_text = getattr(self.ui, f"{current_language_selected}_root_folder_lineedit").text()
            is_ssl_enabled = getattr(self.ui, f"{current_language_selected}_ssl_enabled_checkbox").isChecked()
            ssl_port = getattr(self.ui, f"{current_language_selected}_port_lineedit").text()
            is_chosen = getattr(self.ui, f"{current_language_selected}_radio").isChecked()

            # 2. Xử lý giá trị (ví dụ: root_folder có thể là None)
            root_folder = root_folder_text if root_folder_text.strip() else None
            ssl_port = ssl_port if ssl_port.strip() else None

            # 3. Xây dựng dictionary theo mô hình LanguageSetting
            setting_dict = {
                "language": current_language_selected,
                "selected_version": selected_version,
                "root_folder": root_folder,
                "is_ssl_enabled": is_ssl_enabled,
                "is_chosen": is_chosen,
                "ssl_port": ssl_port,
            }
            required_fields = {
                "language":"Language",
                "selected_version":"Select version",
            }
            for field_key, field_name in required_fields.items():
                if not setting_dict[field_key]:
                    QMessageBox.warning(self,"Thiếu thông tin",f"'{field_name}' không được trống!")
                    return

            result = self.language_core_service.save_changes(setting_dict)
            QMessageBox.information(self, "Thành công", "Đã lưu tất cả thay đổi!") \
                if result else QMessageBox.critical(self,"Lỗi","Có lỗi xảy ra trong quá trình lưu cấu hình!")

        except AttributeError as e:
            # Lỗi này xảy ra nếu tên widget không khớp (ví dụ: 'php_combobox' không tìm thấy)
            QMessageBox.critical(self, "Lỗi UI", f"Không thể lấy dữ liệu từ widget: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Có lỗi xảy ra khi lưu: {str(e)}")

    def init_settings_data(self, language, data):
        try:
            combobox_widget = getattr(self.ui, f"{language}_combobox")
            combobox_widget.setCurrentText(data.selected_version)
            lineedit_widget = getattr(self.ui, f"{language}_root_folder_lineedit")
            lineedit_widget.setText(data.root_folder if data.root_folder is not None else "")
            checkbox_widget = getattr(self.ui, f"{language}_ssl_enabled_checkbox")
            checkbox_widget.setChecked(data.is_ssl_enabled)

        except AttributeError as e:
            QMessageBox.critical(self, "Lỗi Giao diện", f"Không tìm thấy widget cho ngôn ngữ '{language}': {e}")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi khởi tạo dữ liệu cho {language}: {e}")


    def on_language_selected(self, language):
        for str_language, widgets in LanguagesPageController.LANGUAGE_GROUP.items():
            enabled = str_language == language
            for str_widget in widgets:
                widget = getattr(self.ui, str_widget)
                widget.setEnabled(enabled)

            if enabled:
                try:
                    ssl_checkbox = getattr(self.ui, f"{str_language}_ssl_enabled_checkbox")
                    port_lineedit = getattr(self.ui, f"{str_language}_port_lineedit")
                    port_lineedit.setEnabled(ssl_checkbox.isChecked())
                except AttributeError:
                    pass
                else:
                    try:
                        port_lineedit = getattr(self.ui, f"{str_language}_port_lineedit")
                        port_lineedit.setEnabled(False)
                    except AttributeError:
                        pass
        self.dashboard_session.set("language_page_selected", language)

    def _set_ssl_checkbox_toggled(self,language,enabled):
        try:
            port_lineedit = getattr(self.ui, f"{language}_port_lineedit")
            port_lineedit.setEnabled(enabled)
        except AttributeError as e:
            print(f"Lỗi: Không tìm thấy widget cho {language}_port_lineedit: {e}")

    def on_browse_button_clicked(self):
        sender_button_name = self.sender().objectName()
        if sender_button_name not in self.BROWSE_MAP:
            QMessageBox.warning(self, "Lỗi", f"Không tìm thấy cấu hình browse cho: {sender_button_name}")
            return

        config = self.BROWSE_MAP[sender_button_name]
        try:
            dialog_type, target_line_edit_name = config[:2]
            target_line_edit = getattr(self.ui, target_line_edit_name)
        except AttributeError:
            QMessageBox.warning(self, "Lỗi UI", f"Không tìm thấy widget: {target_line_edit_name}")
            return
        except ValueError:
            QMessageBox.warning(self, "Lỗi Cấu hình", f"Cấu hình BROWSE_MAP bị lỗi cho: {sender_button_name}")
            return

        current_path = target_line_edit.text()
        if not os.path.isdir(current_path):  # Kiểm tra xem đường dẫn có hợp lệ không
            current_path = "C:/"  # Mặc định

        selected_path = ""

        if dialog_type == "folder":
            selected_path = QFileDialog.getExistingDirectory(
                self,
                "Chọn thư mục gốc",  # Tiêu đề cửa sổ
                current_path  # Thư mục bắt đầu
            )
        elif dialog_type == "file":
            file_filter = config[2] if len(config) > 2 else "All Files (*)"
            selected_path, _ = QFileDialog.getOpenFileName(
                self,
                "Chọn tệp tin",
                current_path,
                file_filter
            )

        if selected_path:
            normalized_path = os.path.normpath(selected_path)
            target_line_edit.setText(normalized_path)