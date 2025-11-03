from core.repository import WebserverRepository
from core.repository import ProjectRepository
from core.services import ConfigGeneratorService, HostFileService
from core.config import config

def sync_apache_versions():
    WebserverRepository.sync_versions_to_db('apache', str(config.APACHE_ROOT))

def sync_nginx_versions():
    WebserverRepository.sync_versions_to_db('nginx', str(config.NGINX_ROOT))

def sync_language_projects(language:str,root_directory_path:str):
    ProjectRepository.sync_root_directory_to_db(language, root_directory_path)


def sync_update_tld_workflow(new_tld: str):
    """
    Hàm tổng điều phối toàn bộ quá trình thay đổi TLD.
    Đây là hàm mà GUI của bạn sẽ gọi.
    """

    # 1. Kiểm tra quyền Admin (cho file hosts)
    if not HostFileService.is_admin():
        print("LỖI: Cần quyền Admin!")
        # Báo lỗi về GUI
        return False

    try:
        # 2. Cập nhật Database (Vấn đề 1 & 2)
        # (Lưu ý: Phải chạy trước)
        success_db = WebserverRepository.update_tld_in_database(new_tld)
        if not success_db:
            raise Exception("Lỗi cập nhật database")

        # 3. Tái tạo Config Files (Vấn đề 4)
        # (Phải chạy sau khi DB được cập nhật)
        ConfigGeneratorService.regenerate_all_configs()

        # 4. Cập nhật File Hosts (Vấn đề 3)
        # (Phải chạy sau khi DB được cập nhật)
        HostFileService.sync_hosts_file()

        print(f"THÀNH CÔNG: Đã thay đổi TLD thành '{new_tld}' và đồng bộ mọi thứ.")
        return True

    except PermissionError:
        print("Workflow thất bại: Thiếu quyền Admin.")
        # Báo lỗi về GUI
        return False
    except Exception as e:
        print(f"Workflow thất bại: {e}")
        # Báo lỗi về GUI
        return False

# def sync_redis_versions(): ...
# def sync_php_extensions(): ...

ALL_SYNC_TASKS = (
    sync_apache_versions,
    sync_nginx_versions,
    # sync_redis_versions,  # Khi nào làm xong thì bỏ comment
    # sync_php_extensions, # Khi nào làm xong thì bỏ comment
)

# --- Hàm điều phối chính ---
def run_all_startup_syncs():
    print("Bắt đầu quy trình đồng bộ hóa toàn bộ lúc khởi động...")
    for task in ALL_SYNC_TASKS:
        try:
            task()
        except Exception as e:
            print(f"LỖI trong quá trình đồng bộ hóa tác vụ '{task.__name__}': {e}")
    print("Đã hoàn tất tất cả các tác vụ đồng bộ hóa.")