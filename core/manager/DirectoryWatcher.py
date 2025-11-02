import os
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from core.services import SynchronizationService
from core.config import config

class DirectoryChangeHandler(FileSystemEventHandler):
    def __init__(self, create_callback=None, delete_callback=None):
        self._on_create_callback = create_callback
        self._on_delete_callback = delete_callback

    def on_created(self, event):
        if event.is_directory and self._on_create_callback:
            print(f"Handler phát hiện sự kiện tạo mới: {event.src_path}")
            self._on_create_callback() # Gọi cho "chuyên gia"

    def on_deleted(self, event):
        if event.is_directory and self._on_delete_callback:
            print(f"Handler phát hiện sự kiện xóa: {event.src_path}")
            self._on_delete_callback() # Gọi cho "chuyên gia"

_main_observer = None
_dynamic_watches = {}

def start_watching():
    global _main_observer
    if _main_observer:
        return
    _main_observer = Observer()

    apache_handler = DirectoryChangeHandler(create_callback=SynchronizationService.sync_apache_versions,delete_callback=SynchronizationService.sync_apache_versions)
    _main_observer.schedule(apache_handler, str(config.APACHE_ROOT), recursive=False)

    nginx_handler = DirectoryChangeHandler(create_callback=SynchronizationService.sync_nginx_versions,delete_callback=SynchronizationService.sync_nginx_versions)
    _main_observer.schedule(nginx_handler, str(config.NGINX_ROOT), recursive=False)

    # ... làm tương tự cho Redis, PHP, ...

    _main_observer.start()


def add_or_update_dynamic_watch(watch_key: str, path: str, callback_function):

    global _main_observer, _dynamic_watches

    if not _main_observer:
        print("Lỗi: Observer chưa được khởi động. Hãy gọi start_watching() trước.")
        return

    # 1. HỦY theo dõi cũ (nếu có)
    # Kiểm tra xem chúng ta đã lưu "biên bản" cho watch_key này chưa
    if watch_key in _dynamic_watches:
        old_watch = _dynamic_watches.pop(watch_key)  # Lấy biên bản cũ
        print(f"Hủy theo dõi cũ cho '{watch_key}' tại: {old_watch.path}")
        try:
            _main_observer.unschedule(old_watch)
        except Exception as e:
            print(f"Lỗi khi hủy theo dõi {watch_key}: {e}")

    # 2. THÊM theo dõi mới
    if path and os.path.isdir(path):  # Đảm bảo đường dẫn tồn tại
        try:
            print(f"Thêm theo dõi động '{watch_key}' tại: {path}")
            handler = DirectoryChangeHandler(
                create_callback=callback_function,
                delete_callback=callback_function
            )

            # Giao nhiệm vụ và LƯU LẠI "biên bản giao việc" mới
            new_watch = _main_observer.schedule(handler, path, recursive=False)
            _dynamic_watches[watch_key] = new_watch  # Lưu lại biên bản
        except Exception as e:
            print(f"Lỗi khi lên lịch theo dõi động {watch_key} tại {path}: {e}")
    else:
        print(f"Đường dẫn không hợp lệ hoặc không tồn tại, không theo dõi: {path}")


def stop_watching():
    """Dừng Observer khi ứng dụng tắt."""
    global _main_observer
    if _main_observer:
        _main_observer.stop()
        _main_observer.join()  # Đợi luồng kết thúc
        print("Observer đã dừng.")