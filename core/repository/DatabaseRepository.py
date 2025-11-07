import os, sqlite3
from core.config import config
from core.database.model.DatabaseSetting import DatabaseSetting

DB_PATH = config.DB_PATH
DB_SERVICES_PATH = config.DB_SERVICES

def get_all_database_settings()->list[DatabaseSetting]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(""" SELECT * FROM database_settings """)
            rows = cursor.fetchall()

            return [DatabaseSetting(**dict(row)) for row in rows]

    except sqlite3.Error as e:
        print(e)
        raise

def get_current_database_setting()->DatabaseSetting | None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(""" SELECT * FROM database_settings WHERE is_chosen = 1 """)
            row = cursor.fetchone()

            if row:
                return DatabaseSetting(**dict(row))
            return None

    except Exception as e:
        print(e)
        raise

def save_database_setting(setting: DatabaseSetting):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(""" 
                INSERT INTO database_settings (type, port, root_path, base_data_path, is_chosen)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(type) DO UPDATE SET
                    port = excluded.port,
                    root_path = excluded.root_path,
                    base_data_path = excluded.base_data_path,
                    is_chosen = excluded.is_chosen;
             """,(setting.type,setting.port,setting.root_path,
                  setting.base_data_path,setting.is_chosen))
        return True
    except sqlite3.IntegrityError as e:
        print(f"Lỗi trùng port: {e}")
        raise
    except Exception as e:
        print(f"Lỗi khi insert hoặc update database {e}")
        raise

def reset_database_statuses():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(""" UPDATE database_settings SET is_chosen = 0 """)
    except Exception as e:
        print(e)
        raise