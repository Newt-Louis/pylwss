from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()

DB_PATH = PROJECT_ROOT / "core" / "database" / "sqlite.db"

MIGRATIONS_DIR = PROJECT_ROOT / "core" / "database" / "migrate"

APACHE_ROOT = PROJECT_ROOT / "core" / "services" / "webservers" / "bin" / "apache"

NGINX_ROOT = PROJECT_ROOT / "core" / "services" / "webservers" / "bin" / "nginx"

APP_DATA_PORTS = PROJECT_ROOT / "core" / "config"

SSL_PATH = PROJECT_ROOT / "core" / "services" / "webservers" / "open-ssl"