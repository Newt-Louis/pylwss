import os
from jinja2 import Environment, FileSystemLoader

# Chỉ định đường dẫn đến thư mục chứa template
# __file__ là file .py này, '..' đi lên 1 cấp, 'templates' đi vào
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '..', 'config')
JINJA_ENV = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True, lstrip_blocks=True)


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