import sqlite3

def up(cursor: sqlite3.Cursor):
    print("Applying migration: add_is_enabled_to_webserver_settings...")
    cursor.execute("""
                   ALTER TABLE webserver_settings
                       ADD COLUMN is_enabled INTEGER NOT NULL DEFAULT 0;
                   """)


def down(cursor: sqlite3.Cursor):
    print("Reverting migration: add_is_enabled_to_webserver_settings...")
    cursor.execute("ALTER TABLE webserver_settings DROP COLUMN is_enabled;")