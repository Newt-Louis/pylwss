import sqlite3

def up(cursor: sqlite3.Cursor):
    print("Applying migration: create_language_versions_table...")

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS language_versions
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       type TEXT NOT NULL,
                       version TEXT NOT NULL
                   );
                   """)

    # Chèn dữ liệu mẫu
    cursor.execute(
        "INSERT OR IGNORE INTO language_versions (type, version) VALUES ('php', '8.1');")
    cursor.execute(
        "INSERT OR IGNORE INTO language_versions (type, version) VALUES ('php', 'php-8.2.29-nts-Win32-vs16-x64');")
    cursor.execute(
        "INSERT OR IGNORE INTO language_versions (type, version) VALUES ('python', '3.10');")
    cursor.execute(
        "INSERT OR IGNORE INTO language_versions (type, version) VALUES ('python', '3.13');")
    cursor.execute(
        "INSERT OR IGNORE INTO language_versions (type, version) VALUES ('java', 'jdk-21');")
    cursor.execute(
        "INSERT OR IGNORE INTO language_versions (type, version) VALUES ('java', 'jdk-25');")
    cursor.execute(
        "INSERT OR IGNORE INTO language_versions (type, version) VALUES ('nodejs', 'node-v24.11.0-win-x64');")


# Hàm down để hoàn tác
def down(cursor: sqlite3.Cursor):
    print("Reverting migration: create_language_versions_table...")
    cursor.execute("DROP TABLE IF EXISTS language_versions;")