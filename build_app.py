import PyInstaller.__main__, shutil, os, sys

APP_NAME = "pylwssm"
MAIN_FILE = "main.py"
OUTPUT_DIR = "Release_Build"  # Thư mục kết quả cuối cùng
CORE_DIR = "core"  # Thư mục chứa services


def clean_previous_build():
    """Xóa các thư mục build cũ để tránh lỗi"""
    if os.path.exists("build"): shutil.rmtree("build")
    if os.path.exists("dist"): shutil.rmtree("dist")
    if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR)
    if os.path.exists(f"{APP_NAME}.spec"): os.remove(f"{APP_NAME}.spec")


def build_exe():
    """Chạy PyInstaller ở chế độ --onedir (Thư mục)"""
    print("--- Đang đóng gói code Python... ---")
    PyInstaller.__main__.run([
        MAIN_FILE,
        '--name=%s' % APP_NAME,
        '--onedir',  # Quan trọng: Tạo thư mục thay vì 1 file
        '--windowed',  # Ẩn màn hình đen (dành cho App GUI Qt)
        '--noconfirm',
        '--clean',
        '--exclude-module=tkinter',
        '--exclude-module=matplotlib',
    ])


def copy_resources():
    # Đường dẫn file exe được tạo ra trong dist
    src_dist = os.path.join("dist", APP_NAME)

    # Tạo thư mục Release cuối cùng
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Copy toàn bộ nội dung của dist/App vào Release
    # (Gồm file exe và các thư viện dll, qt...)
    for item in os.listdir(src_dist):
        s = os.path.join(src_dist, item)
        d = os.path.join(OUTPUT_DIR, item)
        if os.path.isdir(s):
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    # 2. Copy thư mục core vào Release
    # Hàm os.path.join sẽ copy giữ nguyên cấu trúc thư mục con bên trong
    dest_core = os.path.join(OUTPUT_DIR, "core")

    # ignore=... giúp bỏ qua các file rác như __pycache__ hay .git nếu có
    shutil.copytree(CORE_DIR, dest_core, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.git', '.idea'))

    print(f"--- XONG! Sản phẩm nằm tại thư mục: {OUTPUT_DIR} ---")


if __name__ == "__main__":
    clean_previous_build()
    build_exe()
    copy_resources()