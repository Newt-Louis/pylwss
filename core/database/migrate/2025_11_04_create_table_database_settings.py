import sqlite3

def up(cursor: sqlite3.Cursor):
    print("Applying migration: create_database_settings_table...")

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS database_settings
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       type TEXT,
                       selected_version TEXT,
                       port INTEGER,
                       root_path TEXT,
                       base_data_path TEXT,
                       ssl_cert_path TEXT,
                       require_secure_transport INTEGER DEFAULT 0
                   );
                   """)
# Hàm down để hoàn tác
def down(cursor: sqlite3.Cursor):
    print("Reverting migration: create_database_settings_table...")
    cursor.execute("DROP TABLE IF EXISTS database_settings;")