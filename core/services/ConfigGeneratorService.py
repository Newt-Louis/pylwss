import os, sqlite3
from jinja2 import Environment, FileSystemLoader
from core.config import config
from core.database.model import WebserverSetting
from core.repository import LanguageRepository

# Chỉ định đường dẫn đến thư mục chứa template
# __file__ là file .py này, '..' đi lên 1 cấp, 'templates' đi vào
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'config')
JINJA_ENV = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True, lstrip_blocks=True)
MOCK_PHP_FPM_SOCKET = "127.0.0.1:9000"
MOCK_SSL_CERT_PATH =  os.path.join(config.SSL_PATH,"certificate.crt")
MOCK_SSL_KEY_PATH = os.path.join(config.SSL_PATH,"private.key")

def regenerate_config_for_project(conn: sqlite3.Connection, project_id: int):
    try:
        # 1. Lấy thông tin Webserver chung
        ws_settings = _get_webserver_settings(conn)
        proj_settings = _get_project_details(conn, project_id)
        if proj_settings["language"].lower() == "php":
            proj_settings["project_path"] += "/public"
        context = {
            "http_port": ws_settings["http_port"],
            "ssl_port": ws_settings["ssl_port"],
            "domain": proj_settings["domain"],
            "document_root": proj_settings["project_path"].replace("\\","/"),
            "access_log_path": ws_settings["alp_path"].replace("\\","/"),
            "error_log_path": ws_settings["elp_path"].replace("\\","/"),
            "is_ssl_enabled": bool(proj_settings.get("is_ssl_enabled", 0)),
            "app_port": proj_settings["app_port"],

            "project_type": _map_project_type(proj_settings["language"]),

            "php_fpm_socket": MOCK_PHP_FPM_SOCKET,
            "ssl_certificate_path": MOCK_SSL_CERT_PATH,
            "ssl_key_path": MOCK_SSL_KEY_PATH,
        }

        server_name = ws_settings["server_name"].lower()
        if server_name == 'nginx':
            template_name = 'nginx_vhost.j2'
        elif server_name == 'apache':
            template_name = 'apache_vhost.j2'
        else:
            raise ValueError(f"Webserver không hỗ trợ: {server_name}")

        output_filename = f"{context['domain']}.conf"
        output_path = os.path.join(
            ws_settings["sites_enabled_path"],
            proj_settings["language"].lower(),
            output_filename
        )
        print(f"Bắt đầu sinh config cho: {context['domain']}...")
        success = generate_config_file(template_name, context, output_path)
        if success:
            print(f"Hoàn tất sinh config cho project ID: {project_id} tại {output_path}")
        else:
            raise Exception("Hàm generate_config_file báo lỗi.")
    except Exception as e:
        print(f"LỖI NGHIÊM TRỌNG khi sinh config cho project ID {project_id}: {e}")

def generate_config_file(template_name: str, context: dict, output_path: str):
    """
    Tạo file config từ một khuôn mẫu Jinja2.

    Args:
        template_name: Tên file mẫu (ví dụ: 'nginx_vhost.j2').
        context: Một dict chứa tất cả các biến (ví dụ: domain, document_root).
        output_path: Nơi lưu file .conf hoàn chỉnh.
    """
    try:
        template = JINJA_ENV.get_template(template_name)
        rendered_config = template.render(context)

        # Đảm bảo thư mục đầu ra tồn tại
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_config)
        print(f"Tạo file config thành công tại: {output_path}")
        return True
    except Exception as e:
        print(f"Lỗi khi tạo file config: {e}")
        return False


def remove_config_for_project(conn: sqlite3.Connection, project_id: int):
    try:
        # 1. Lấy thông tin cần thiết để *tìm* file config
        ws_settings = _get_webserver_settings(conn)
        proj_settings = _get_project_details(conn, project_id)

        # 2. Xây dựng lại đường dẫn file config CHÍNH XÁC như lúc tạo
        output_filename = f"{proj_settings['domain']}.conf"
        output_path = os.path.join(
            ws_settings["sites_enabled_path"],
            proj_settings["language"].lower(),
            output_filename
        )

        # 3. Thực hiện xóa file
        if os.path.exists(output_path):
            os.remove(output_path)
            print(f"Đã xóa file config thành công: {output_path}")
        else:
            print(f"Cảnh báo: Không tìm thấy file config để xóa tại: {output_path}")

    except Exception as e:
        print(f"LỖI khi xóa file config cho project ID {project_id}: {e}")


def regenerate_all_configs():
    """
    Xóa tất cả file config cũ và tạo lại toàn bộ từ DB.
    Hàm này phải được gọi SAU KHI DB đã được cập nhật TLD mới.
    """
    print("Bắt đầu tái tạo toàn bộ file config...")

    # 1. Lấy tất cả dự án
    try:
        with sqlite3.connect(config.DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # 1. Lấy thông tin webserver (để biết đường dẫn)
            ws_settings = _get_webserver_settings(conn)  # Dùng hàm private bạn đã có
            sites_enabled_path = ws_settings['sites_enabled_path']

            # 2. Xóa SẠCH tất cả file .conf trong các thư mục con
            # (Đây là cách đơn giản nhất để xử lý file cũ)
            cursor.execute("SELECT DISTINCT language FROM projects")
            languages = [row['language'] for row in cursor.fetchall()]

            for lang in languages:
                lang_dir = os.path.join(sites_enabled_path, lang.lower())
                if os.path.isdir(lang_dir):
                    for f in os.listdir(lang_dir):
                        if f.endswith('.conf'):
                            os.remove(os.path.join(lang_dir, f))
            print("Đã xóa tất cả file config cũ.")

            # 3. Lấy TẤT CẢ project ID
            cursor.execute("SELECT id FROM projects")
            project_ids = [row['id'] for row in cursor.fetchall()]

            # 4. Tái tạo từng file
            for project_id in project_ids:
                # Gọi hàm gốc của bạn
                regenerate_config_for_project(conn, project_id)

        print("Hoàn tất tái tạo toàn bộ config.")

    except Exception as e:
        print(f"LỖI NGHIÊM TRỌNG khi tái tạo config: {e}")
        raise

def _map_project_type(language:str) -> str:
    lang = language.lower()
    if lang == 'php':
         return 'static_php'
    elif lang in ['python', 'nodejs', 'node', 'deno', 'bun']:
        return 'proxy'
    else:
        return 'static_php'


def _get_webserver_settings(conn: sqlite3.Connection) -> dict:
    """
    Lấy cài đặt webserver đang hoạt động.
    (Giả định chỉ có 1 dòng cài đặt webserver)
    """
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT server_name, http_port, ssl_port, alp_path, elp_path, sites_enabled_path
                   FROM webserver_settings
                   WHERE is_enabled = 1
                   LIMIT 1
                   """)
    row = cursor.fetchone()
    if not row:
        raise Exception("Không tìm thấy cấu hình trong 'webserver_settings'")

    # Chuyển đổi tuple (row) thành dict
    return dict(zip([col[0] for col in cursor.description], row))


def _get_project_details(conn: sqlite3.Connection, project_id: int) -> dict:
    """
    Hàm trợ giúp lấy thông tin chi tiết của dự án (project và language).
    """
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT p.project_path, p.language, p.app_port, p.domain, ls.is_ssl_enabled
                   FROM projects p
                   LEFT JOIN language_settings ls ON p.language = ls.language
                   WHERE p.id = ?
                   """, (project_id,))

    proj_row = cursor.fetchone()
    if not proj_row:
        raise Exception(f"Không tìm thấy dự án (ID: {project_id}).")

    return dict(zip([col[0] for col in cursor.description], proj_row))

def regenerate_main_nginx_config(settings: WebserverSetting):
    try:
        # 1. Xác định các đường dẫn dựa trên 'sites_enabled_path'
        # (ví dụ: D:/.../sites-available)
        conf_dir = os.path.dirname(settings.sites_enabled_path)

        template_path = os.path.join(TEMPLATE_DIR, 'nginx.conf.j2')
        output_path = os.path.join(conf_dir, 'nginx.conf')  # File sẽ bị ghi đè

        template = JINJA_ENV.get_template('nginx.conf.j2')

        if not os.path.exists(template_path):
            print(f"LỖI: Không tìm thấy template nginx.conf.j2 tại: {template_path}")
            return

        languages_version = LanguageRepository.get_all_language_versions()
        languages = {language for language in languages_version.keys()}
        sites_path = settings.sites_enabled_path.replace("\\", "/")

        context = {
            "sites_enabled_path": sites_path,
            "language_folders": languages,
            "access_log_path": settings.alp_path.replace("\\", "/") if settings.alp_path else None,
            "error_log_path": settings.elp_path.replace("\\", "/") if settings.elp_path else None,
            "http_port": settings.http_port,
        }

        rendered_config = template.render(context)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_config)

        print(f"SERVICE: Tạo file nginx.conf thành công tại: {output_path}")

    except Exception as e:
        print(f"LỖI NGHIÊM TRỌNG khi tạo file nginx.conf: {e}")

def regenerate_main_apache_config(settings: WebserverSetting):
    try:
        # 1. Xác định các đường dẫn dựa trên 'sites_enabled_path'
        # (ví dụ: D:/.../sites-available)
        conf_dir = os.path.dirname(settings.sites_enabled_path)

        template_path = os.path.join(TEMPLATE_DIR, 'httpd.conf.j2')
        output_path = os.path.join(conf_dir, 'httpd.conf')  # File sẽ bị ghi đè

        template = JINJA_ENV.get_template('httpd.conf.j2')

        if not os.path.exists(template_path):
            print(f"LỖI: Không tìm thấy template httpd.conf.j2 tại: {template_path}")
            return

        languages_version = LanguageRepository.get_all_language_versions()
        languages = {language for language in languages_version.keys()}
        sites_path = settings.sites_enabled_path.replace("\\", "/")

        context = {
            "sites_enabled_path": sites_path,
            "language_folders": languages,
            "access_log_path": settings.alp_path.replace("\\", "/") if settings.alp_path else None,
            "error_log_path": settings.elp_path.replace("\\", "/") if settings.elp_path else None,
            "base_directory": os.path.dirname(conf_dir),
            "http_port": settings.http_port,
        }

        rendered_config = template.render(context)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_config)

        print(f"SERVICE: Tạo file httpd.conf thành công tại: {output_path}")

    except Exception as e:
        print(f"LỖI NGHIÊM TRỌNG khi tạo file httpd.conf: {e}")