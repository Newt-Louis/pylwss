import sqlite3
from core.config import config

def up(cursor: sqlite3.Cursor):
    print("Applying migration: create_webserver_settings_table...")
    nginx_executable_path = config.NGINX_ROOT / "nginx-1.28.0" / "nginx.exe"
    nginx_sites_enabled_path = config.NGINX_ROOT / "nginx-1.28.0" / "conf" / "sites-available"
    apache_executable_path = config.APACHE_ROOT / "httpd-2.4.63-250207-win64-VS17" / "bin" / "httpd.exe"
    apache_sites_enabled_path = config.APACHE_ROOT / "httpd-2.4.63-250207-win64-VS17" / "conf" / "sites-available"
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS webserver_settings
                   (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       server_name        TEXT NOT NULL UNIQUE,
                       selected_version   TEXT,
                       executable_path    TEXT,
                       sites_enabled_path TEXT,
                       tld_template       TEXT DEFAULT '.test',
                       http_port          INTEGER,
                       ssl_port           INTEGER,
                       alp_path           TEXT,
                       elp_path           TEXT
                   );
                   """)

    # Chèn dữ liệu mẫu
    cursor.execute(
        "INSERT OR IGNORE INTO webserver_settings (server_name, http_port, ssl_port, executable_path, sites_enabled_path) VALUES ('apache', 8080, 443, ?, ?);",
        (nginx_executable_path, nginx_sites_enabled_path))
    cursor.execute(
        "INSERT OR IGNORE INTO webserver_settings (server_name, http_port, ssl_port, executable_path, sites_enabled_path) VALUES ('nginx', 80, 8443, ?, ?);",
        (apache_executable_path,apache_sites_enabled_path))


# Hàm down để hoàn tác
def down(cursor: sqlite3.Cursor):
    print("Reverting migration: create_webserver_table...")
    cursor.execute("DROP TABLE IF EXISTS webserver_settings;")