from PySide6.QtWidgets import QWidget, QRadioButton, QFileDialog, QMessageBox
from .WebserverServiceController import WebserverServiceController
from ui.windows.origin_interface import Ui_WebserverPage


class WebserverPageController(QWidget):
    BROWSE_MAP = {
        "apache_excutable_browseButton": ("file","apache_excutable_lineEdit","(*.exe)"),
        "apache_sites_enabled_browseButton": ("folder","apache_sites_enabled_lineEdit",""),
        "apache_alp_browseButton": ("folder","apache_alp_lineEdit",""),
        "apache_elp_browseButton": ("folder","apache_elp_lineEdit",""),
        "nginx_excutable_browseButton": ("file", "nginx_excutable_lineEdit", "(*.exe)"),
        "nginx_sites_enabled_browseButton": ("folder", "nginx_sites_enabled_lineEdit", ""),
        "nginx_alp_browseButton": ("folder", "nginx_alp_lineEdit", ""),
        "nginx_elp_browseButton": ("folder", "nginx_elp_lineEdit", ""),
    }
    WIDGET_MAP = {
        'selected_version': ('select_version_combobox', 'QComboBox'),
        'executable_path': ('excutable_lineEdit', 'QLineEdit'),
        'sites_enabled_path': ('sites_enabled_lineEdit', 'QLineEdit'),
        'http_port': ('listen_port_lineEdit', 'QLineEdit'),
        'tld_template': ('config_tld_lineEdit', 'QLineEdit'),
        'alp_path': ('alp_lineEdit', 'QLineEdit'),
        'elp_path': ('elp_lineEdit', 'QLineEdit'),
    }
    def __init__(self, model=None):
        super().__init__()
        self.model = model
        self.service_controller = WebserverServiceController()
        self.ui = Ui_WebserverPage()
        self.ui.setupUi(self)

        # Gắn sự kiện
        self.ui.apache_radio.clicked.connect(self.on_webserver_changed)
        self.ui.nginx_radio.clicked.connect(self.on_webserver_changed)
        self.ui.webserver_save_change_buttonbox.clicked.connect(self.on_save_changes)
        for button in self.findChildren(QWidget):
            name = button.objectName()
            #Gắn sự kiện cho tất cả nút Browse
            if name.endswith("_browseButton"):
                button.clicked.connect(self.on_browse_button_clicked)

        # Hiển thị thông tin đang được lưu
        try:
            current_data = self.service_controller.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            current_data = None

        if current_data is not None:
            for webserver in current_data:
                server_name = webserver.server_name
                handler_function_name = f"on_{server_name}_selected"
                setradio_checked = f"{server_name}_radio"
                if hasattr(self, handler_function_name):
                    handler_function = getattr(self, handler_function_name)
                    handler_function(webserver)
                else:
                    print(f"Không tìm thấy phương thức {handler_function_name} tương ứng")
                if webserver.is_enabled:
                    radio_button = getattr(self.ui, setradio_checked)
                    radio_button.setChecked(True)
                    self.on_webserver_changed()

        # Điền thông tin phiên bản
        versions = self.service_controller.load_webservers_version()
        self.ui.apache_select_version_combobox.addItems([version["version"] for version in versions["apache"]])
        self.ui.nginx_select_version_combobox.addItems([version["version"] for version in versions["nginx"]])


    def on_save_changes(self):
        config_data = {}
        active_server_prefix = ""

        if self.ui.apache_radio.isChecked():
            active_server_prefix = "apache_"
            config_data["type"] = "apache"
        elif self.ui.nginx_radio.isChecked():
            active_server_prefix = "nginx_"
            config_data["type"] = "nginx"

        # Sử dụng getattr để lấy widget một cách linh động dựa trên prefix
        config_data['selected_version'] = getattr(self.ui, f"{active_server_prefix}select_version_combobox").currentText()
        config_data['executable_path'] = getattr(self.ui,f"{active_server_prefix}excutable_lineEdit").text().strip()
        config_data['sites_enabled_path'] = getattr(self.ui,f"{active_server_prefix}sites_enabled_lineEdit").text().strip()
        config_data['listen_port'] = getattr(self.ui, f"{active_server_prefix}listen_port_lineEdit").text().strip()
        config_data['tld'] = getattr(self.ui, f"{active_server_prefix}config_tld_lineEdit").text().strip()
        config_data['access_log_path'] = getattr(self.ui, f"{active_server_prefix}alp_lineEdit").text().strip()
        config_data['error_log_path'] = getattr(self.ui, f"{active_server_prefix}elp_lineEdit").text().strip()

        required_fields = {
            'executable_path': "Excutable path",
            'sites_enabled_path': "Sites-Enabled path",
            'listen_port': "Listen port",
            'selected_version': "Version",
        }

        for field_key, field_name in required_fields.items():
            if not config_data[field_key]:
                QMessageBox.warning(self, "Thiếu thông tin", f"'{field_name}' không được để trống!")
                return

        result = self.service_controller.save_changes(config_data)
        QMessageBox.information(self, "Thành công", "Đã lưu cấu hình webserver thành công!") \
            if result else QMessageBox.critical(self,"Lỗi","Có lỗi xảy ra trong quá trình lưu cấu hình!")

    def on_apache_selected(self,data):
        self._populate_form_with_data(data)

    def on_nginx_selected(self,data):
        self._populate_form_with_data(data)

    def _populate_form_with_data(self, data):
        # 1. Xác định tiền tố dựa trên dữ liệu (ví dụ: 'apache_')
        prefix = f"{data.server_name}_"

        # 2. Lặp qua bản đồ WIDGET_MAP
        for data_attribute, (widget_suffix, widget_type) in self.__class__.WIDGET_MAP.items():
            try:
                # 3. Dùng getattr để lấy giá trị từ đối tượng data
                # Ví dụ: data.executable_path
                value = getattr(data, data_attribute)

                # 4. Xây dựng tên đầy đủ của widget
                # Ví dụ: 'apache_excutable_lineEdit'
                widget_name = f"{prefix}{widget_suffix}"

                # 5. Dùng getattr để lấy đối tượng widget thực sự từ self.ui
                widget = getattr(self.ui, widget_name)

                # 6. Điền dữ liệu dựa trên loại widget
                if widget_type == 'QLineEdit':
                    widget.setText(str(value) if value is not None else "")
                elif widget_type == 'QComboBox':
                    widget.setCurrentText(value if value is not None else "")

            except AttributeError:
                # Bỏ qua nếu không tìm thấy widget hoặc thuộc tính, tránh crash
                print(f"Cảnh báo: Không tìm thấy widget '{widget_name}' hoặc thuộc tính '{data_attribute}'.")

    def set_group_enabled(self, prefix, enabled):
        for widget in self.findChildren(QWidget):
            if widget.objectName().startswith(prefix):
                if isinstance(widget,QRadioButton):
                    continue
                else:
                    widget.setEnabled(enabled)

    def on_webserver_changed(self):
        if self.ui.apache_radio.isChecked():
            self.set_group_enabled("apache_", True)
            self.set_group_enabled("nginx_", False)
        elif self.ui.nginx_radio.isChecked():
            self.set_group_enabled("apache_", False)
            self.set_group_enabled("nginx_", True)

    def on_browse_button_clicked(self):
        """Xử lý khi click bất kỳ nút Browse nào"""
        sender = self.sender()
        name = sender.objectName()
        if name not in self.__class__.BROWSE_MAP:
            return

        browse_type, lineedit_name, file_filter = self.__class__.BROWSE_MAP[name]
        line_edit = getattr(self.ui, lineedit_name)

        if browse_type == "file":
            file_path, _ = QFileDialog.getOpenFileName(self, "Chọn file", "", file_filter)
            if file_path:
                line_edit.setText(file_path)
        else:  # folder
            folder = QFileDialog.getExistingDirectory(self, "Chọn thư mục", "")
            if folder:
                line_edit.setText(folder)


    # Các widget hiện đang có trong WebserverPage
    # Apache:
    #         self.ui.apache_select_version_combobox
    #         self.ui.apache_excutable_lineEdit
    #         self.ui.apache_excutable_browseButton
    #         self.ui.apache_sites_enabled_lineEdit
    #         self.ui.apache_sites_enabled_browseButton
    #         self.ui.apache_listen_port_lineEdit
    #         self.ui.apache_config_tld_lineEdit
    #         self.ui.apache_alp_lineEdit
    #         self.ui.apache_alp_browseButton
    #         self.ui.apache_elp_lineEdit
    #         self.ui.apache_elp_browseButton
    # Nginx
    #         self.ui.nginx_select_version_combobox
    #         self.ui.nginx_excutable_lineEdit
    #         self.ui.nginx_excutable_browseButton
    #         self.ui.nginx_sites_enabled_lineEdit
    #         self.ui.nginx_sites_enabled_browseButton
    #         self.ui.nginx_listen_port_lineEdit
    #         self.ui.nginx_config_tld_lineEdit
    #         self.ui.nginx_alp_lineEdit
    #         self.ui.nginx_alp_browseButton
    #         self.ui.nginx_elp_lineEdit
    #         self.ui.nginx_elp_browseButton