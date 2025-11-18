import sqlite3

def up(cursor: sqlite3.Cursor):
    print("Applying migration: create_webserver_versions_table...")

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS webserver_versions
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       type TEXT NOT NULL,
                       versions TEXT NOT NULL
                   );
                   """)

    # Chèn dữ liệu mẫu
    cursor.execute(
        "INSERT OR IGNORE INTO webserver_versions (type, versions) VALUES ('apache', 'httpd-2.4.63-250207-win64-VS17');")
    cursor.execute(
        "INSERT OR IGNORE INTO webserver_versions (type, versions) VALUES ('nginx', 'nginx-1.28.0');")


# Hàm down để hoàn tác
def down(cursor: sqlite3.Cursor):
    print("Reverting migration: create_webserver_versions_table...")
    cursor.execute("DROP TABLE IF EXISTS webserver_versions;")