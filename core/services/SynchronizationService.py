from core.repository import WebserverRepository
from core.repository import ProjectRepository
from core.services import ConfigGeneratorService
from core.config import config

def sync_apache_versions():
    WebserverRepository.sync_versions_to_db('apache', str(config.APACHE_ROOT))

def sync_nginx_versions():
    WebserverRepository.sync_versions_to_db('nginx', str(config.NGINX_ROOT))

def sync_language_projects(language:str,root_directory_path:str):
    ProjectRepository.sync_root_directory_to_db(language, root_directory_path)

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