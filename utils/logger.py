"""
Logger Module
Cấu hình logging cho toàn bộ ứng dụng
"""

import logging
import sys
import os
from pathlib import Path
from datetime import datetime


def setup_logger(
    name: str,
    log_file: str = None,
    level: str = 'INFO',
    format_string: str = None
) -> logging.Logger:
    """
    Setup logger với file và console handlers
    
    Args:
        name: Tên logger
        log_file: Path đến log file
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_string: Custom format string
    
    Returns:
        Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Format
    if format_string is None:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    formatter = logging.Formatter(format_string)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (nếu có log_file)
    if log_file:
        # Tạo thư mục logs nếu chưa có
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get logger với cấu hình default
    
    Args:
        name: Tên logger (thường dùng __name__)
    
    Returns:
        Logger instance
    """
    # Tạo log directory
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Log file name theo ngày
    log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    
    return setup_logger(
        name=name,
        log_file=str(log_file),
        level=os.getenv('LOG_LEVEL', 'INFO')
    )


class ColoredFormatter(logging.Formatter):
    """Colored formatter cho console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        """Format log record với màu sắc"""
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


def get_colored_logger(name: str) -> logging.Logger:
    """
    Get logger với colored output
    
    Args:
        name: Tên logger
    
    Returns:
        Logger với colored console output
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if logger.handlers:
        return logger
    
    # Console handler với colored formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    colored_formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(colored_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    return logger


if __name__ == "__main__":
    # Test logger
    logger = get_colored_logger(__name__)
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
