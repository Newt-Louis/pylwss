import sqlite3

def up(cursor: sqlite3.Cursor):
    print("Applying migration: rename_versions_to_version...")
    cursor.execute("""
                   ALTER TABLE webserver_versions
                       RENAME COLUMN versions TO version;
                   """)


def down(cursor: sqlite3.Cursor):
    print("Reverting migration: rename_versions_to_version...")
    cursor.execute("ALTER TABLE webserver_versions RENAME COLUMN version TO versions;")