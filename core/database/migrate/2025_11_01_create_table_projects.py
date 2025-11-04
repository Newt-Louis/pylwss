import sqlite3

def up(cursor: sqlite3.Cursor):
    print("Applying migration: create_projects_table...")

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS projects
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       project_name TEXT,
                       language TEXT,
                       project_path TEXT,
                       app_port INTEGER,
                       domain TEXT,
                       is_enabled BOOLEAN
                   );
                   """)

# Hàm down để hoàn tác
def down(cursor: sqlite3.Cursor):
    print("Reverting migration: create_projects_table...")
    cursor.execute("DROP TABLE IF EXISTS projects;")