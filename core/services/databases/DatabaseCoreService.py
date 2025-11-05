import os
from pathlib import Path
from core.database.model import DatabaseSetting
from core.config import config
from core.repository import DatabaseRepository

class DatabaseCoreService:
    def __init__(self):
        self._DB_SERVICES_PATH = config.DB_SERVICES
    def save_settings(self,settings: DatabaseSetting):
        print("Chuẩn bị lưu cấu hình database")

    def generate_ini_file(self,type):
        if type == "mysql":
            mysql_template = self.mysql_template()
        else:
            print("Chưa có DBMS này trong ứng dụng, cần cài đặt thêm!")

    def mysql_template(self, settings):
        settings = {
            "port":3306,
            "data_directory": self._DB_SERVICES_PATH / "mysql-8.4.6-winx64" / "data",
            "sql_mode":"NO_ENGINE_SUBTITUTION",
            "auth_plugin":"mysql_native_password",
        }
        datadir = settings['data_directory'].replace('\\', '/')
        ini_content = f""" 
                            [mysqld]
                            port = {settings['port']}
                            datadir = "{datadir}"
                            bind-address = 127.0.0.1
                            default_authentication_plugin = {settings['auth_plugin']}
                            sql_mode = "{settings['sql_mode']}"
                        """
        config_path = self._DB_SERVICES_PATH / "mysql-8.4.6-winx64" /  "mysql.ini"
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(ini_content)
            print(f"Tạo file {config_path} thành công!")
        except IOError as e:
            print(f"Lỗi khi ghi file: {e}")