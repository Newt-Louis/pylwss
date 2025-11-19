import subprocess, json, zipfile, io, shutil, requests
from pathlib import Path
from core.config import config
from core.database.model.tools.ToolsSetting import ToolsSetting
from core.manager.EventBus import event_bus
from core.repository import ToolsRepository


class ToolsCoreService:
    def __init__(self):
        self.running_processes = {}
        self.default_json_path = config.TOOL_SERVICES.parent.resolve()
        self._tool_configs = {}
        self.reload_configs_from_db()
        event_bus.app_exit.connect(self._listener_app_exit)

    @property
    def tool_configs(self):
        return self._tool_configs

    def install_default_tool(self, tool_type: str):
        # 1. Đọc file JSON mặc định
        if not self.default_json_path.exists():
            return {"status": False, "message": "Không tìm thấy file cấu hình initialize_tools.json"}

        try:
            with open(self.default_json_path, 'r', encoding='utf-8') as f:
                init_data = json.load(f)
        except Exception as e:
            return {"status": False, "message": f"Lỗi đọc JSON: {str(e)}"}

        if tool_type not in init_data:
            return {"status": False, "message": f"Tool '{tool_type}' không có trong file cấu hình JSON."}

        tool_info = init_data[tool_type]
        download_url = tool_info.get("download_url")
        json_cwd_dir = tool_info.get("cwd_dir", "")  # Đường dẫn có chứa $$

        # 2. Xử lý đường dẫn thư mục đích (Thay thế $$)
        # config.TOOL_SERVICES là đường dẫn .../bin
        target_folder_str = json_cwd_dir.replace("$$", str(config.TOOL_SERVICES))
        target_folder_path = Path(target_folder_str)

        # 3. Tải và giải nén
        try:
            if not download_url:
                return {"status": False, "message": "Không tìm thấy URL tải xuống trong cấu hình."}

            # Tạo thư mục bin nếu chưa có
            config.TOOL_SERVICES.mkdir(parents=True, exist_ok=True)

            print(f"Đang tải xuống từ: {download_url}")
            success = self._download_and_extract(download_url, config.TOOL_SERVICES)

            if not success:
                return {"status": False, "message": "Lỗi trong quá trình tải hoặc giải nén file."}

        except Exception as e:
            return {"status": False, "message": f"Lỗi cài đặt: {str(e)}"}

        # 4. Chuẩn bị dữ liệu để lưu vào SQLite
        # Lưu ý: root_path trong DB nên lưu đường dẫn folder chứa tool (cwd)
        new_setting = {
            "type": tool_type,
            "port": tool_info.get("port", 0000),
            "root_path": str(target_folder_path),  # Lưu đường dẫn thực tế trên máy
            "is_chosen": True  # Đánh dấu là đang được chọn sử dụng
        }

        # 5. Lưu vào DB thông qua Repository
        try:
            self.save_tools_config([new_setting])
        except Exception as e:
            return {"status": False, "message": f"Lỗi khi lưu DB: {str(e)}"}

        self.reload_configs_from_db()

        return {"status": True, "message": f"Cài đặt {tool_type} thành công!"}

    def reload_configs_from_db(self):
        try:
            settings_from_db = ToolsRepository.get_all_tools_settings()

            if not settings_from_db:
                return

            for setting in settings_from_db:
                root_path = Path(setting.root_path)

                exe_name = ""
                if setting.type == "redis":
                    exe_name = "redis-server.exe"
                # elif setting.type == "mailsender":
                #     exe_name = "mail.exe"

                self.tool_configs[setting.type] = {
                    "cwd_dir": root_path,
                    "exe_path": root_path / exe_name,
                    "port": setting.port # Các tool khác không có port thì sẽ là 0 hoặc 0000
                }

            print(f"Đã reload cấu hình tools: {list(self.tool_configs.keys())}")

        except Exception as e:
            print(f"Lỗi khi reload config từ DB: {e}")

    def get_init_tools_settings(self):
        try:
            return ToolsRepository.get_all_tools_settings()
        except:
            raise

    def save_tools_config(self,raw_data):
        data = [ToolsSetting(**tool_settings) for tool_settings in raw_data]
        try:
            result = ToolsRepository.save_tools_setting(data)
            if result:
                self.reload_configs_from_db()
                event_bus.tools_saved(data)
        except:
            raise

    def start_redis_service(self):
        if "redis" not in self.tool_configs:
            return {"status": False, "message": "Redis chưa được cài đặt hoặc chưa cấu hình đường dẫn."}

        redis_config = self.tool_configs["redis"]
        exe_path = redis_config["exe_path"]
        cwd_dir = redis_config["cwd_dir"]
        port = str(redis_config.get("port", 6379))

        if not exe_path.exists():
            return {"status": False, "message": f"Không tìm thấy 'redis-server.exe' tại đường dẫn: {self.tool_configs["redis"]["exe_path"]}"}

        # poll() == None nghĩa là tiến trình đang chạy
        if "redis" in self.running_processes and self.running_processes["redis"].poll() is None:
            return {"status":True,"message": f"Redis service đã chạy (PID: {self.running_processes["redis"].pid})."}

        try:
            CREATE_NO_WINDOW = 0x08000000
            command = [str(exe_path),"--port",port]
            process = subprocess.Popen(
                command,  # Lệnh cần chạy (phải là list)
                cwd=str(cwd_dir),  # Đặt thư mục làm việc
                creationflags=CREATE_NO_WINDOW,  # Cờ để ẩn cửa sổ console
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.running_processes["redis"] = process
            return {"status":True,"message":f"Redis service đã khởi động thành công (PID: {process.pid})."}

        except FileNotFoundError:
            raise
        except Exception as e:
            raise

    def stop_redis_service(self):
        if "redis" not in self.running_processes:
            return {"status":False, "message":"Redis service không đang chạy (hoặc không được quản lý)."}

        process = self.running_processes["redis"]
        pid = process.pid

        if process.poll() is not None:
            del self.running_processes["redis"]
            return {"status":True,"message":f"Redis (PID: {pid}) đã dừng trước đó. Đang dọn dẹp..."}

        try:
            process.terminate()
            try:
                process.wait(timeout=5)  # Chờ 5 giây
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)

            del self.running_processes["redis"]
            return {"status":True,"message":"Redis đã dừng"}

        except Exception as e:
            print(f"Lỗi khi dừng Redis (PID: {pid}): {e}")
            if "redis" in self.running_processes:
                del self.running_processes["redis"]
            raise

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

    def _download_and_extract(self, url: str, extract_to: Path) -> bool:
        try:
            # Stream=True để tải file lớn không bị tràn RAM
            response = requests.get(url, stream=True)
            response.raise_for_status()

            # Dùng io.BytesIO để giải nén trực tiếp từ RAM mà không cần lưu file zip tạm
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                z.extractall(extract_to)

            return True
        except Exception as e:
            print(f"Download/Extract Error: {e}")
            return False

tools_core_service = ToolsCoreService()