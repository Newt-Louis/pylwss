import os, sqlite3
from jinja2 import Environment, FileSystemLoader

# Chỉ định đường dẫn đến thư mục chứa template
# __file__ là file .py này, '..' đi lên 1 cấp, 'templates' đi vào
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'config')
JINJA_ENV = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True, lstrip_blocks=True)
APP_CONFIG_OUTPUT_DIR = "D:/laragon-clone/etc/webserver/sites-enabled"
MOCK_PHP_FPM_SOCKET = "127.0.0.1:9000"
MOCK_SSL_CERT_PATH = "D:/laragon-clone/etc/ssl/my_cert.crt"
MOCK_SSL_KEY_PATH = "D:/laragon-clone/etc/ssl/my_key.key"

def regenerate_config_for_project(conn: sqlite3.Connection, project_id: int):
    """
    Hàm chính: Tự động sinh file config cho một dự án cụ thể.
    Được gọi khi tạo/cập nhật dự án.
    """
    try:
        # 1. Lấy thông tin Webserver chung
        ws_settings = _get_webserver_settings(conn)

        # 2. Lấy thông tin Project và Language (JOIN 2 bảng)
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT p.project_path,
                              p.language,
                              p.app_port,
                              p.domain,
                              ls.is_ssl_enabled
                       FROM projects p
                                JOIN language_settings ls ON p.language = ls.language
                       WHERE p.id = ?
                       """, (project_id,))

        proj_row = cursor.fetchone()
        if not proj_row:
            raise Exception(f"Không tìm thấy dự án (ID: {project_id}) hoặc cài đặt ngôn ngữ tương ứng.")

        proj_settings = dict(zip([col[0] for col in cursor.description], proj_row))

        # 3. Xây dựng Context hoàn chỉnh cho Jinja2
        context = {
            "http_port": ws_settings["http_port"],
            "ssl_port": ws_settings["ssl_port"],
            "domain": proj_settings["domain"],
            "document_root": proj_settings["project_path"],
            "access_log_path": ws_settings["alp_path"],
            "error_log_path": ws_settings["elp_path"],
            "is_ssl_enabled": bool(proj_settings["is_ssl_enabled"]),
            "app_port": proj_settings["app_port"],

            "project_type": _map_project_type(proj_settings["language"]),

            "php_fpm_socket": MOCK_PHP_FPM_SOCKET,
            "ssl_certificate_path": MOCK_SSL_CERT_PATH,
            "ssl_key_path": MOCK_SSL_KEY_PATH,
        }

        # 4. Xác định template và đường dẫn output
        server_name = ws_settings["server_name"].lower()
        if server_name == 'nginx':
            template_name = 'nginx_vhost.j2'
        elif server_name == 'apache':
            template_name = 'apache_vhost.j2'
        else:
            raise ValueError(f"Webserver không hỗ trợ: {server_name}")

        # Đường dẫn file config đầu ra, ví dụ: .../sites-enabled/my-project.test.conf
        output_filename = f"{context['domain']}.conf"
        output_path = os.path.join(APP_CONFIG_OUTPUT_DIR, output_filename)

        # 5. Gọi hàm generator của bạn
        print(f"Bắt đầu sinh config cho: {context['domain']}...")
        success = generate_config_file(template_name, context, output_path)

        if success:
            print(f"Hoàn tất sinh config cho project ID: {project_id}")
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

def _map_project_type(language:str) -> str:
    lang = language.lower()
    if lang == 'php':
         return 'static_php'
    elif lang in ['python', 'nodejs', 'node', 'deno', 'bun']:
        return 'proxy'
    else:
        return 'static_php'


def _get_webserver_settings(conn: sqlite3.Connection,server) -> dict:
    """
    Lấy cài đặt webserver đang hoạt động.
    (Giả định chỉ có 1 dòng cài đặt webserver)
    """
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT server_name,
                          http_port,
                          ssl_port,
                          alp_path,
                          elp_path
                   FROM webserver_settings
                    WHERE server_name = ?
                   LIMIT 1
                   """,(server,))
    row = cursor.fetchone()
    if not row:
        raise Exception("Không tìm thấy cấu hình trong 'webserver_settings'")

    # Chuyển đổi tuple (row) thành dict
    return dict(zip([col[0] for col in cursor.description], row))