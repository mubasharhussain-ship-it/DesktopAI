"""
Utility Functions Module
Common utility functions used across the application.
"""

import os
import sys
import time
import logging
import requests
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logging() -> logging.Logger:
    """Setup logging configuration."""
    try:
        # Create logs directory
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configure root logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        
        # Remove existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler with rotation
        file_handler = RotatingFileHandler(
            log_dir / "app.log",
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # Create application logger
        app_logger = logging.getLogger(__name__)
        app_logger.info("Logging setup completed")
        
        return app_logger
        
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        # Return basic logger
        return logging.getLogger(__name__)


def check_internet_connection(url: str = "http://www.google.com", timeout: int = 5) -> bool:
    """Check if internet connection is available."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except:
        return False


def wait_for_internet(url: str = "http://www.google.com", timeout: int = 300, check_interval: int = 5) -> bool:
    """Wait for internet connection to become available."""
    logger = logging.getLogger(__name__)
    logger.info(f"Waiting for internet connection (timeout: {timeout}s)")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if check_internet_connection(url):
            logger.info("Internet connection established")
            return True
        
        logger.debug(f"No internet connection, retrying in {check_interval}s...")
        time.sleep(check_interval)
    
    logger.warning(f"Internet connection not available after {timeout}s")
    return False


def ensure_directory_exists(directory_path: str) -> bool:
    """Ensure a directory exists, create it if it doesn't."""
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Error creating directory {directory_path}: {str(e)}")
        return False


def get_system_info() -> dict:
    """Get basic system information."""
    try:
        import platform
        import psutil
        
        return {
            "platform": platform.platform(),
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "disk_usage_gb": round(psutil.disk_usage('/').total / (1024**3), 2)
        }
    except Exception as e:
        logging.getLogger(__name__).error(f"Error getting system info: {str(e)}")
        return {}


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system usage."""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename.strip()


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"


def get_free_disk_space(path: str = ".") -> int:
    """Get free disk space in bytes."""
    try:
        import shutil
        return shutil.disk_usage(path).free
    except Exception:
        return 0


def cleanup_old_files(directory: str, pattern: str = "*", max_age_days: int = 7, max_count: Optional[int] = None):
    """Clean up old files in a directory."""
    try:
        logger = logging.getLogger(__name__)
        directory_path = Path(directory)
        
        if not directory_path.exists():
            return
        
        # Get all matching files
        files = list(directory_path.glob(pattern))
        
        # Filter by age
        current_time = time.time()
        old_files = []
        
        for file_path in files:
            if file_path.is_file():
                file_age = current_time - file_path.stat().st_mtime
                file_age_days = file_age / (24 * 3600)
                
                if file_age_days > max_age_days:
                    old_files.append((file_path, file_age_days))
        
        # Sort by age (oldest first)
        old_files.sort(key=lambda x: x[1], reverse=True)
        
        # Apply max count limit if specified
        if max_count is not None and len(files) > max_count:
            # Keep only the newest max_count files
            all_files_by_time = sorted(files, key=lambda x: x.stat().st_mtime, reverse=True)
            files_to_remove = all_files_by_time[max_count:]
            
            # Add to old_files list
            for file_path in files_to_remove:
                if (file_path, 0) not in old_files:  # Avoid duplicates
                    old_files.append((file_path, 0))
        
        # Remove old files
        removed_count = 0
        for file_path, age in old_files:
            try:
                file_path.unlink()
                removed_count += 1
                logger.debug(f"Removed old file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to remove {file_path}: {str(e)}")
        
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} old files from {directory}")
    
    except Exception as e:
        logging.getLogger(__name__).error(f"Error cleaning up old files: {str(e)}")


def is_admin() -> bool:
    """Check if the current process is running with admin privileges."""
    try:
        import ctypes
        import sys
        if sys.platform == 'win32':
            return ctypes.windll.shell32.IsUserAnAdmin()
        return False
    except:
        return False


def get_windows_version() -> Optional[str]:
    """Get Windows version information."""
    try:
        import platform
        return platform.platform()
    except:
        return None


def kill_process_by_name(process_name: str) -> bool:
    """Kill process by name (be very careful with this!)."""
    try:
        import psutil
        logger = logging.getLogger(__name__)
        
        killed = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'].lower() == process_name.lower():
                    proc.kill()
                    logger.warning(f"Killed process: {process_name} (PID: {proc.info['pid']})")
                    killed = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return killed
    except Exception as e:
        logging.getLogger(__name__).error(f"Error killing process {process_name}: {str(e)}")
        return False


def validate_coordinates(x: int, y: int) -> tuple:
    """Validate and clamp coordinates to screen bounds."""
    try:
        import pyautogui
        screen_width, screen_height = pyautogui.size()
        
        # Clamp coordinates to screen bounds
        x = max(0, min(x, screen_width - 1))
        y = max(0, min(y, screen_height - 1))
        
        return (x, y)
    except:
        # Return original coordinates if pyautogui fails
        return (x, y)


def create_backup(source_path: str, backup_suffix: str = ".backup") -> bool:
    """Create a backup copy of a file."""
    try:
        source = Path(source_path)
        if not source.exists():
            return False
        
        backup_path = source.with_suffix(source.suffix + backup_suffix)
        
        # Copy file
        import shutil
        shutil.copy2(source, backup_path)
        
        logging.getLogger(__name__).info(f"Created backup: {backup_path}")
        return True
        
    except Exception as e:
        logging.getLogger(__name__).error(f"Error creating backup: {str(e)}")
        return False


def safe_json_load(file_path: str) -> dict:
    """Safely load JSON file with error handling."""
    try:
        import json
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.getLogger(__name__).error(f"Error loading JSON from {file_path}: {str(e)}")
        return {}


def safe_json_save(data: dict, file_path: str) -> bool:
    """Safely save data to JSON file."""
    try:
        import json
        
        # Create backup if file exists
        if os.path.exists(file_path):
            create_backup(file_path)
        
        # Ensure directory exists
        ensure_directory_exists(os.path.dirname(file_path))
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Error saving JSON to {file_path}: {str(e)}")
        return False


def get_application_path() -> str:
    """Get the application's root directory path."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def setup_signal_handlers():
    """Setup signal handlers for graceful shutdown."""
    import signal
    logger = logging.getLogger(__name__)
    
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        # The main application should handle this
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
