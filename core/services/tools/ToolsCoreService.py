import subprocess
from core.config import config
from core.database.model.tools.ToolsSetting import ToolsSetting
from core.manager.EventBus import event_bus
from core.repository import ToolsRepository


class ToolsCoreService:
    def __init__(self):
        self.running_processes = {}
        self.tool_configs = {
            "redis": {
                "exe_path": config.TOOL_SERVICES / "Redis-x64-5.0.14.1" / "redis-server.exe",
                "cwd_dir": config.TOOL_SERVICES / "Redis-x64-5.0.14.1",
                "port": 6379
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

    def save_tools_config(self,raw_data):
        data = [ToolsSetting(**tool_settings) for tool_settings in raw_data]
        try:
            return ToolsRepository.save_tools_setting(data)
        except:
            raise

    def start_redis_service(self):
        redis_config = self.tool_configs["redis"]
        exe_path = redis_config["exe_path"]
        cwd_dir = redis_config["cwd_dir"]
        port = str(redis_config.get("port", 6379))

        if not exe_path.exists():
            print(f"LỖI: Không tìm thấy 'redis-server.exe' tại đường dẫn:")
            print(f"{self.tool_configs["redis"]["exe_path"]}")
            return False

        # poll() == None nghĩa là tiến trình đang chạy
        if "redis" in self.running_processes and self.running_processes["redis"].poll() is None:
            print(f"Redis service đã chạy (PID: {self.running_processes["redis"].pid}).")
            return True

        try:
            CREATE_NO_WINDOW = 0x08000000
            command = [
                str(exe_path),
                "--port",
                port
            ]
            process = subprocess.Popen(
                command,  # Lệnh cần chạy (phải là list)
                cwd=str(cwd_dir),  # Đặt thư mục làm việc
                creationflags=CREATE_NO_WINDOW,  # Cờ để ẩn cửa sổ console
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.running_processes["redis"] = process
            print(f"Redis service đã khởi động thành công (PID: {process.pid}).")
            return True

        except FileNotFoundError:
            print(f"LỖI: FileNotFoundError. Đường dẫn có đúng không?")
            print(f"{self.tool_configs["redis"]["exe_path"]}")
            return False
        except Exception as e:
            print(f"LỖI không xác định khi khởi động Redis: {e}")
            if "redis" in self.running_processes:
                del self.running_processes["redis"]
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