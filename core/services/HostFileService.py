import os, ctypes
import sqlite3
from core.config import config  # Giả định

DB_PATH = config.DB_PATH
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
MARKER = "# MANAGED_BY_PYLWSSM"
def is_admin():
    """Kiểm tra xem script có đang chạy với quyền Admin trên Windows không."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False # Không phải Windows

def sync_hosts_file():
    """
    Đồng bộ tất cả domain trong DB vào file hosts.
    Hàm này đọc file, xóa các dòng cũ (có marker), và thêm các dòng mới.
    """
    if not os.access(HOSTS_PATH, os.W_OK):
        print(f"LỖI: Không có quyền ghi vào file hosts. Cần chạy bằng quyền Admin.")
        # Bạn nên raise Exception ở đây để báo về GUI
        raise PermissionError("Không có quyền ghi vào file hosts.")

    # 1. Lấy tất cả domain MỚI NHẤT từ DB
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # Giả sử bạn chỉ muốn đồng bộ các dự án đang "enabled"
            cursor.execute("SELECT domain FROM projects WHERE is_enabled = 1 AND domain IS NOT NULL")
            all_domains = [row['domain'] for row in cursor.fetchall()]
    except Exception as e:
        print(f"Lỗi khi đọc domain từ DB: {e}")
        return

    # 2. Đọc file hosts và lọc bỏ các dòng cũ CỦA TA
    clean_lines = []
    try:
        with open(HOSTS_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                if MARKER not in line:
                    clean_lines.append(line.rstrip())
    except FileNotFoundError:
        print("Không tìm thấy file hosts")
        return

    # 3. Thêm các dòng mới vào
    for domain in all_domains:
        new_line = f"127.0.0.1\t{domain}\t{MARKER}"
        clean_lines.append(new_line)

    # 4. Ghi đè lại file hosts
    try:
        with open(HOSTS_PATH, 'w', encoding='utf-8') as f:
            f.write("\n".join(clean_lines) + "\n")
        print(f"Cập nhật file hosts thành công cho {len(all_domains)} domain.")
    except Exception as e:
        print(f"LỖI NGHIÊM TRỌNG khi ghi file hosts: {e}")
        raise