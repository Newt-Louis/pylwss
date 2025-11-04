import logging, os
from logging.handlers import RotatingFileHandler
from core.config import config

# Định nghĩa đường dẫn lưu log (bạn có thể lấy từ file config)
LOG_DIR = config.LOG_PATH
LOG_FILE = os.path.join(LOG_DIR, 'app.log')

# Đảm bảo thư mục log tồn tại
os.makedirs(LOG_DIR, exist_ok=True)


class Logger:
    def __init__(self, logger_name='AppLogger', log_file=LOG_FILE, level=logging.DEBUG):
        """
        Khởi tạo Logger.

        Args:
            logger_name (str): Tên của logger.
            log_file (str): Đường dẫn đầy đủ đến file log.
            level (int): Cấp độ log (ví dụ: logging.DEBUG, logging.INFO).
        """
        # 1. Tạo đối tượng logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(level)

        # 2. Tạo định dạng (formatter)
        # Ví dụ: 2025-11-04 16:30:00,123 - INFO - Đây là thông báo
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 3. Tạo File Handler
        # RotatingFileHandler: Tự động xoay vòng file log khi nó quá lớn
        # maxBytes=5*1024*1024: 5 MB
        # backupCount=2: Giữ lại 2 file log cũ (app.log.1, app.log.2)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=2,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # 4. Tạo Console Handler (để in ra cả terminal khi dev)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)

        # 5. Thêm handlers vào logger
        # (Kiểm tra để tránh thêm handler nhiều lần nếu khởi tạo lại)
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message, exc_info=False):
        """Ghi log lỗi. Đặt exc_info=True để tự động thêm thông tin exception."""
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message, exc_info=False):
        self.logger.critical(message, exc_info=exc_info)

logger = Logger()