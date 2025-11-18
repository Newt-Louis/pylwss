import sqlite3

def up(cursor: sqlite3.Cursor):
    print("Applying migration: create_database_settings_table...")

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS tools_settings
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       type TEXT UNIQUE,
                       port INTEGER UNIQUE,
                       root_path TEXT,
                       is_chosen INTEGER DEFAULT 0
                   );
                   """)
# Hàm down để hoàn tác
def down(cursor: sqlite3.Cursor):
    print("Reverting migration: create_database_settings_table...")
    cursor.execute("DROP TABLE IF EXISTS tools_settings;")