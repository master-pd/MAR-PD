import logging
import os
from datetime import datetime
from colorlog import ColoredFormatter

class Logger:
    def __init__(self, name: str = "SafeUserBot"):
        self.logger = logging.getLogger(name)
        self.setup_logger()
    
    def setup_logger(self):
        """লগার সেটআপ"""
        # লগ লেভেল
        self.logger.setLevel(logging.DEBUG)
        
        # লগ ফরম্যাট
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        color_format = "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        # কনসোল হ্যান্ডলার
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # কালার ফরম্যাট
        formatter = ColoredFormatter(
            color_format,
            datefmt="%Y-%m-%d %H:%M:%S",
            reset=True,
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(formatter)
        
        # ফাইল হ্যান্ডলার
        os.makedirs("logs", exist_ok=True)
        file_handler = logging.FileHandler(f"logs/bot_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        
        # হ্যান্ডলার যোগ
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        """ইনফো লগ"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """ওয়ার্নিং লগ"""
        self.logger.warning(message)
    
    def error(self, message: str, exc_info=False):
        """এরর লগ"""
        self.logger.error(message, exc_info=exc_info)
    
    def debug(self, message: str):
        """ডিবাগ লগ"""
        self.logger.debug(message)
    
    def critical(self, message: str):
        """ক্রিটিকাল লগ"""
        self.logger.critical(message)

# গ্লোবাল লগার
log = Logger()