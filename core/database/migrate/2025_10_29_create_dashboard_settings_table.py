import sqlite3

def up(cursor: sqlite3.Cursor):
    print("Applying migration: create_dashboard_settings_table...")

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS dashboard_settings (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       service TEXT,
                       type TEXT,
                       version TEXT,
                       is_running INTEGER NOT NULL DEFAULT 0
                   );
                   """)
    # Chèn dữ liệu mẫu
    cursor.execute("INSERT OR IGNORE INTO dashboard_settings (service, type, version) VALUES ('database', 'MySQL', '');")
    cursor.execute("INSERT OR IGNORE INTO dashboard_settings (service, type, version) VALUES ('language', 'PHP', '');")
    cursor.execute("INSERT OR IGNORE INTO dashboard_settings (service, type, version) VALUES ('webserver', 'nginx', '');")
    cursor.execute("INSERT OR IGNORE INTO dashboard_settings (service, type, version) VALUES ('tool', 'telnet', '');")
    cursor.execute("INSERT OR IGNORE INTO dashboard_settings (service, type, version) VALUES ('all', '', '');")

# Hàm down để hoàn tác
def down(cursor: sqlite3.Cursor):
    print("Reverting migration: create_dashboard_settings_table...")
    cursor.execute("DROP TABLE IF EXISTS dashboard_settings;")