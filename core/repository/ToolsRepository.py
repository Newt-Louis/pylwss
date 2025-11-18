import os, sqlite3
from core.config import config
from core.database.model import ToolsSetting

DB_PATH = config.DB_PATH
DB_SERVICES_PATH = config.DB_SERVICES

def get_all_tools_settings()->list[ToolsSetting]:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(""" SELECT * FROM tools_settings """)
            rows = cursor.fetchall()

            return [ToolsSetting(**dict(row)) for row in rows]

    except sqlite3.Error as e:
        print(e)
        raise

def get_chosen_tools_settings()->ToolsSetting | None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(""" SELECT * FROM tools_settings WHERE is_chosen = 1 """)
            row = cursor.fetchone()

            if row:
                return ToolsSetting(**dict(row))
            return None

    except Exception as e:
        print(e)
        raise

def save_tools_setting(settings: list[ToolsSetting]):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.executemany(""" 
                INSERT INTO tools_settings (type, port, root_path, is_chosen)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(type) DO UPDATE SET
                    port = excluded.port,
                    root_path = excluded.root_path,
                    is_chosen = excluded.is_chosen;
             """,[(s.type,s.port,s.root_path,s.is_chosen) for s in settings])
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
            cursor.execute(""" UPDATE tools_settings SET is_chosen = 0 """)
    except Exception as e:
        print(e)
        raise