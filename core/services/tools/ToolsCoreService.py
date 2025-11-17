import subprocess
from core.config import config
from core.manager.EventBus import event_bus


class ToolsCoreService:
    def __init__(self):
        self.redis_process = None
        self.running_processes = {}
        self.tool_configs = {
            "redis": {
                "exe_path": config.TOOL_SERVICES / "Redis-x64-5.0.14.1" / "redis-server.exe",
                "cwd_dir": config.TOOL_SERVICES / "Redis-x64-5.0.14.1"
            },
            # "mailsender": {
            #     "exe_path": config.TOOL_SERVICES / "MailSender" / "mail.exe",
            #     "cwd_dir": config.TOOL_SERVICES / "MailSender"
            # },
            # "notepad++": {
            #     "exe_path": Path("C:/Program Files/Notepad++/notepad++.exe"),
            #     "cwd_dir": Path("C:/Program Files/Notepad++")
            # }
        }

        event_bus.app_exit.connect(self._listener_app_exit)

    def start_redis_service(self):
        # Kiểm tra xem file thực thi có tồn tại không
        if not self.tool_configs["redis"]["exe_path"].exists():
            print(f"LỖI: Không tìm thấy 'redis-server.exe' tại đường dẫn:")
            print(f"{self.tool_configs["redis"]["exe_path"]}")
            return False

        # poll() == None nghĩa là tiến trình đang chạy
        if "redis" in self.running_processes and self.running_processes["redis"].poll() is None:
            print(f"Redis service đã chạy (PID: {self.redis_process.pid}).")
            return True

        try:
            CREATE_NO_WINDOW = 0x08000000
            self.redis_process = subprocess.Popen(
                [str(self.tool_configs["redis"]["exe_path"])],  # Lệnh cần chạy (phải là list)
                cwd=str(self.tool_configs["redis"]["cwd_dir"]),  # Đặt thư mục làm việc
                creationflags=CREATE_NO_WINDOW,  # Cờ để ẩn cửa sổ console
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            print(f"Redis service đã khởi động thành công (PID: {self.redis_process.pid}).")
            return True

        except FileNotFoundError:
            print(f"LỖI: FileNotFoundError. Đường dẫn có đúng không?")
            print(f"{self.tool_configs["redis"]["exe_path"]}")
            return False
        except Exception as e:
            print(f"LỖI không xác định khi khởi động Redis: {e}")
            self.redis_process = None
            return False

    def stop_redis_service(self):
        if "redis" not in self.running_processes:
            print("Redis service không đang chạy (hoặc không được quản lý).")
            return False

        process = self.running_processes["redis"]
        pid = process.pid

        if process.poll() is not None:
            print(f"Redis (PID: {pid}) đã dừng trước đó. Đang dọn dẹp...")
            del self.running_processes["redis"]
            return True

        try:
            print(f"Đang dừng Redis service (PID: {pid})...")
            process.terminate()
            try:
                process.wait(timeout=5)  # Chờ 5 giây
                print(f"Redis (PID: {pid}) đã dừng (terminate).")
            except subprocess.TimeoutExpired:
                print(f"Terminate thất bại, buộc dừng (kill) Redis (PID: {pid}).")
                process.kill()
                process.wait(timeout=2)
                print(f"Redis (PID: {pid}) đã dừng (kill).")

            del self.running_processes["redis"]
            return True

        except Exception as e:
            print(f"Lỗi khi dừng Redis (PID: {pid}): {e}")
            if "redis" in self.running_processes:
                del self.running_processes["redis"]
            return False

    def stop_all_services(self):
        if "redis" in self.running_processes:
            self.stop_redis_service()

        # Gọi stop mailsender
        # if "mailsender" in self.running_processes:
        #     self.stop_mailsender_service()

        # ... thêm các dịch vụ khác ở đây ...

        print("--- Hoàn tất dọn dẹp tất cả dịch vụ ---")

    def _listener_app_exit(self):
        self.stop_all_services()

tools_core_service = ToolsCoreService()