import os, sqlite3
from core.config import config
from core.database.model.DatabaseSetting import DatabaseSetting

DB_PATH = config.DB_PATH
DB_SERVICES_PATH = config.DB_SERVICES

def get_all_database_settings()->list[DatabaseSetting] | None:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(""" SELECT * FROM database_settings """)
            rows = cursor.fetchall()

            if rows:
                return [DatabaseSetting(**dict(row)) for row in rows]
            return None

    except Exception as e:
        print(e)
        raise e

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
        raise e