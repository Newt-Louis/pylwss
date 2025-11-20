import sys
from pathlib import Path

def get_project_root():
    if getattr(sys, 'frozen', False):
        # Chạy EXE (PyInstaller)
        # sys.executable là đường dẫn đầy đủ đến file pylwss.exe
        # .parent sẽ lấy thư mục chứa file exe đó
        return Path(sys.executable).parent
    else:
        # Chạy Code Python thường (.py)
        return Path(__file__).parent.parent.parent.resolve()

PROJECT_ROOT = get_project_root()

DB_PATH = PROJECT_ROOT / "core" / "database" / "sqlite.db"

MIGRATIONS_DIR = PROJECT_ROOT / "core" / "database" / "migrate"

APACHE_ROOT = PROJECT_ROOT / "core" / "services" / "webservers" / "bin" / "apache"

NGINX_ROOT = PROJECT_ROOT / "core" / "services" / "webservers" / "bin" / "nginx"

APP_DATA_PORTS = PROJECT_ROOT / "core" / "config"

SSL_PATH = PROJECT_ROOT / "core" / "services" / "webservers" / "open-ssl"

LOG_PATH = PROJECT_ROOT / "tests" / "logs"

DB_SERVICES = PROJECT_ROOT / "core" / "services" / "databases" / "database_management_systems"

TOOL_SERVICES = PROJECT_ROOT / "core" / "services" / "tools" / "bin"

PHP_EXEC_PATH = PROJECT_ROOT / "core" / "services" / "languages" / "bin"