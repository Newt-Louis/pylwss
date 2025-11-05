import os, ctypes, sqlite3
from core.utils import Helper
from core.config import config

DB_PATH = config.DB_PATH
OS_TYPE = Helper.get_os_type()
if OS_TYPE == "windows":
    HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
elif OS_TYPE == "darwin" or OS_TYPE == "linux":
    HOSTS_PATH = "/etc/hosts"
else:
    HOSTS_PATH = None
MARKER = "# MANAGED_BY_PYLWSSM"
def is_admin():
    """Kiểm tra xem script có đang chạy với quyền Admin trên Windows không."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False # Không phải Windows

def sync_hosts_file():
    if HOSTS_PATH is None or not os.access(HOSTS_PATH, os.W_OK):
        print(f"LỖI: Không có quyền ghi vào file hosts. Cần chạy bằng quyền Admin.")
        raise PermissionError("Không có quyền ghi vào file hosts.")

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT domain FROM projects AS p JOIN language_settings AS ls on p.language = ls.language WHERE p.domain IS NOT NULL AND ls.is_chosen = 1")
            all_domains = [row['domain'] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Lỗi khi đọc domain từ DB: {e}")
        return

    clean_lines = []
    try:
        with open(HOSTS_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if MARKER not in line:
                    clean_lines.append(line.rstrip())
    except FileNotFoundError:
        print("Không tìm thấy file hosts")
        return

    for domain in all_domains:
        new_line = f"127.0.0.1\t{domain}\t{MARKER}"
        clean_lines.append(new_line)

    try:
        with open(HOSTS_PATH, 'w', encoding='utf-8') as f:
            f.write("\n".join(clean_lines) + "\n")
        print(f"Cập nhật file hosts thành công cho {len(all_domains)} domain.")
    except Exception as e:
        print(f"LỖI NGHIÊM TRỌNG khi ghi file hosts: {e}")
        raise