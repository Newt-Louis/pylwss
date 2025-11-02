import json
import os
from threading import Lock  # Đảm bảo an toàn khi nhiều luồng cùng truy cập


class PortManager:
    _instance = None
    _lock = Lock()  # Khóa luồng (thread-safe)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                # Kiểm tra lại bên trong khóa để tránh race condition
                if cls._instance is None:
                    cls._instance = super(PortManager, cls).__new__(cls)
        return cls._instance

    def __init__(self,
                 config_path: str = 'ports.json',
                 start_port: int = 8000,
                 end_port: int = 8999):
        """
        Khởi tạo Trình quản lý cổng.

        Args:
            config_path (str): File JSON để lưu trạng thái các cổng.
            start_port (int): Cổng proxy bắt đầu.
            end_port (int): Cổng proxy kết thúc.
        """
        # Ngăn __init__ chạy lại trên Singleton
        if hasattr(self, '_initialized'):
            return

        with self._lock:
            if hasattr(self, '_initialized'):
                return

            self.config_path = config_path
            self.start_port = start_port
            self.end_port = end_port

            # `used_ports` sẽ là một dict: {"project_name": 8001, ...}
            self.used_ports = self._load_ports_from_config()
            self._initialized = True

    def _load_ports_from_config(self) -> dict:
        """Tải danh sách cổng đã dùng từ file JSON."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Lỗi: File {self.config_path} bị hỏng. Tạo mới.")
                return {}
        return {}

    def _save_ports_to_config(self):
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.used_ports, f, indent=4)
        except IOError as e:
            print(f"Lỗi nghiêm trọng: Không thể ghi file port: {e}")

    def get_next_available_port(self, project_name: str) -> int | None:
        with self._lock:  # Đảm bảo an toàn luồng
            # 1. Kiểm tra xem dự án này đã được cấp cổng chưa
            if project_name in self.used_ports:
                return self.used_ports[project_name]

            # 2. Tìm cổng trống tiếp theo
            current_used_ports = set(self.used_ports.values())

            for port in range(self.start_port, self.end_port + 1):
                if port not in current_used_ports:
                    # Tìm thấy! Cấp phát cổng này
                    self.used_ports[project_name] = port
                    self._save_ports_to_config()
                    return port

            # Nếu chạy hết vòng lặp mà không tìm thấy
            print("Lỗi: Đã hết cổng proxy để cấp phát!")
            return None

    def release_port(self, project_name: str) -> bool:
        with self._lock:
            if project_name in self.used_ports:
                del self.used_ports[project_name]
                self._save_ports_to_config()
                return True

            return False

    def get_port_for_project(self, project_name: str) -> int | None:
        return self.used_ports.get(project_name)