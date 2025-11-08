import sqlite3
from core.config import config
from core.database.model import DashboardSetting

DB_PATH = config.DB_PATH

def get_all_dashboard_settings()->list[DashboardSetting] | None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dashboard_settings")
            rows = cursor.fetchall()

            if len(rows) != 0:
                return [DashboardSetting(**dict(row)) for row in rows]

            return None
    except sqlite3.Error as e:
        print(e)
        raise

def save_webserver(dashboard_setting: DashboardSetting):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           UPDATE dashboard_settings
                           SET type    = ?,
                               version = ?,
                               is_running= ?
                           WHERE service = ?
                            """,(
                                dashboard_setting.type,
                                dashboard_setting.version,
                                dashboard_setting.is_running,
                                dashboard_setting.service
                           ))

            print("Đã lưu thông tin webserver vào database")
            return True
    except Exception as e:
        print(e)
        return False

def save_database(dashboard_setting: DashboardSetting):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           UPDATE dashboard_settings
                           SET type    = ?,
                               version = ?,
                               is_running= ?
                           WHERE service = ?
                            """,(
                                dashboard_setting.type,
                                dashboard_setting.version,
                                dashboard_setting.is_running,
                                dashboard_setting.service
                           ))

            return True
    except Exception as e:
        print(e)
        return False

def save_language(dashboard_setting: DashboardSetting):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           UPDATE dashboard_settings
                           SET type    = ?,
                               version = ?,
                               is_running= ?
                           WHERE service = ?
                            """,(
                                dashboard_setting.type,
                                dashboard_setting.version,
                                dashboard_setting.is_running,
                                dashboard_setting.service
                           ))

            print("Đã lưu thông tin language vào database")
            return True
    except Exception as e:
        print(e)
        return False

def save_tool(tool_info):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           UPDATE dashboard_settings
                           SET type    = ?,
                               version = ?
                           WHERE service = 'tool'
                            """,(
                               tool_info.type,
                               tool_info.version,
                           ))

            print("Đã lưu thông tin tool vào database")
            return True
    except Exception as e:
        print(e)
        return False

def save_network(network_info):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           UPDATE dashboard_settings
                           SET type    = ?,
                               version = ?
                           WHERE service = 'network'
                            """,(
                               network_info.type,
                               network_info.version,
                           ))

            print("Đã lưu thông tin network vào database")
            return True
    except Exception as e:
        print(e)
        return False

def save_serivce_statuses(services_info: dict):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.executemany("""
                           UPDATE dashboard_settings
                           SET is_running = ?
                           WHERE service = ?
                           """,
                           [(is_running, service_name) for service_name, is_running in services_info])

            print("Đã lưu trạng thái mới cho các dịch vụ")
            return True
    except Exception as e:
        print(e)
        return False

def reset_dashboard_statuses():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(""" UPDATE dashboard_settings SET is_running = 0 """)
    except Exception as e:
        print(e)
