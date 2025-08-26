"""
Configuration Manager Module
Manages application configuration and settings.
"""

import os
import logging
from pathlib import Path
from configparser import ConfigParser
from typing import Any, Optional


class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self):
        """Initialize configuration manager."""
        self.logger = logging.getLogger(__name__)
        self.config_file = Path("config/settings.ini")
        self.config = ConfigParser()
        
        # Ensure config directory exists
        self.config_file.parent.mkdir(exist_ok=True)
        
        # Load configuration
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file or create default."""
        try:
            if self.config_file.exists():
                self.config.read(self.config_file, encoding='utf-8')
                self.logger.info("Configuration loaded successfully")
            else:
                self._create_default_config()
                
        except Exception as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            self._create_default_config()
    
    def _create_default_config(self):
        """Create default configuration file."""
        try:
            # LLM Settings
            self.config['LLM'] = {
                'model': 'llava',  # Default model for vision tasks
                'temperature': '0.1',
                'max_tokens': '1000',
                'timeout': '60'
            }
            
            # Automation Settings
            self.config['AUTOMATION'] = {
                'command_delay': '2.0',  # Seconds between commands
                'polling_interval': '1.0',  # Seconds between file checks
                'failsafe': 'true',  # Enable pyautogui failsafe
                'pause': '0.1',  # Default pause between actions
                'max_retries': '3'
            }
            
            # Screen Capture Settings
            self.config['SCREEN'] = {
                'screenshot_quality': '95',
                'max_screenshots': '50',
                'compression': 'PNG'
            }
            
            # Safety Settings
            self.config['SAFETY'] = {
                'enable_safety_checks': 'true',
                'max_click_distance': '50',
                'safe_mode': 'true',
                'log_all_actions': 'true'
            }
            
            # Logging Settings
            self.config['LOGGING'] = {
                'level': 'INFO',
                'max_log_size': '10485760',  # 10MB
                'backup_count': '5',
                'log_to_console': 'true'
            }
            
            # Network Settings
            self.config['NETWORK'] = {
                'internet_check_url': 'http://www.google.com',
                'internet_check_timeout': '5',
                'max_wait_for_internet': '300'  # 5 minutes
            }
            
            # Save default configuration
            self._save_config()
            self.logger.info("Created default configuration")
            
        except Exception as e:
            self.logger.error(f"Error creating default configuration: {str(e)}")
    
    def _save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
        except Exception as e:
            self.logger.error(f"Error saving configuration: {str(e)}")
    
    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """Get configuration value."""
        try:
            return self.config.get(section, key, fallback=str(fallback) if fallback is not None else None)
        except Exception:
            return fallback
    
    def getint(self, section: str, key: str, fallback: int = 0) -> int:
        """Get integer configuration value."""
        try:
            return self.config.getint(section, key, fallback=fallback)
        except Exception:
            return fallback
    
    def getfloat(self, section: str, key: str, fallback: float = 0.0) -> float:
        """Get float configuration value."""
        try:
            return self.config.getfloat(section, key, fallback=fallback)
        except Exception:
            return fallback
    
    def getboolean(self, section: str, key: str, fallback: bool = False) -> bool:
        """Get boolean configuration value."""
        try:
            return self.config.getboolean(section, key, fallback=fallback)
        except Exception:
            return fallback
    
    def set(self, section: str, key: str, value: Any):
        """Set configuration value."""
        try:
            if not self.config.has_section(section):
                self.config.add_section(section)
            
            self.config.set(section, key, str(value))
            self._save_config()
            
        except Exception as e:
            self.logger.error(f"Error setting configuration value: {str(e)}")
    
    # Convenience methods for common settings
    def get_llm_model(self) -> str:
        """Get LLM model name."""
        return self.get('LLM', 'model', 'llava')
    
    def get_llm_temperature(self) -> float:
        """Get LLM temperature."""
        return self.getfloat('LLM', 'temperature', 0.1)
    
    def get_llm_max_tokens(self) -> int:
        """Get LLM max tokens."""
        return self.getint('LLM', 'max_tokens', 1000)
    
    def get_llm_timeout(self) -> int:
        """Get LLM timeout in seconds."""
        return self.getint('LLM', 'timeout', 60)
    
    def get_command_delay(self) -> float:
        """Get delay between commands in seconds."""
        return self.getfloat('AUTOMATION', 'command_delay', 2.0)
    
    def get_polling_interval(self) -> float:
        """Get polling interval for command file checks."""
        return self.getfloat('AUTOMATION', 'polling_interval', 1.0)
    
    def is_failsafe_enabled(self) -> bool:
        """Check if automation failsafe is enabled."""
        return self.getboolean('AUTOMATION', 'failsafe', True)
    
    def get_automation_pause(self) -> float:
        """Get default pause between automation actions."""
        return self.getfloat('AUTOMATION', 'pause', 0.1)
    
    def get_max_retries(self) -> int:
        """Get maximum number of retries for failed actions."""
        return self.getint('AUTOMATION', 'max_retries', 3)
    
    def get_screenshot_quality(self) -> int:
        """Get screenshot quality (0-100)."""
        return self.getint('SCREEN', 'screenshot_quality', 95)
    
    def get_max_screenshots(self) -> int:
        """Get maximum number of screenshots to keep."""
        return self.getint('SCREEN', 'max_screenshots', 50)
    
    def is_safety_enabled(self) -> bool:
        """Check if safety checks are enabled."""
        return self.getboolean('SAFETY', 'enable_safety_checks', True)
    
    def get_max_click_distance(self) -> int:
        """Get maximum allowed click distance in pixels."""
        return self.getint('SAFETY', 'max_click_distance', 50)
    
    def is_safe_mode(self) -> bool:
        """Check if safe mode is enabled."""
        return self.getboolean('SAFETY', 'safe_mode', True)
    
    def should_log_all_actions(self) -> bool:
        """Check if all actions should be logged."""
        return self.getboolean('SAFETY', 'log_all_actions', True)
    
    def get_log_level(self) -> str:
        """Get logging level."""
        return self.get('LOGGING', 'level', 'INFO')
    
    def get_max_log_size(self) -> int:
        """Get maximum log file size in bytes."""
        return self.getint('LOGGING', 'max_log_size', 10485760)
    
    def get_log_backup_count(self) -> int:
        """Get number of log backup files to keep."""
        return self.getint('LOGGING', 'backup_count', 5)
    
    def should_log_to_console(self) -> bool:
        """Check if logging to console is enabled."""
        return self.getboolean('LOGGING', 'log_to_console', True)
    
    def get_internet_check_url(self) -> str:
        """Get URL for internet connectivity checks."""
        return self.get('NETWORK', 'internet_check_url', 'http://www.google.com')
    
    def get_internet_check_timeout(self) -> int:
        """Get timeout for internet checks in seconds."""
        return self.getint('NETWORK', 'internet_check_timeout', 5)
    
    def get_max_wait_for_internet(self) -> int:
        """Get maximum time to wait for internet connection."""
        return self.getint('NETWORK', 'max_wait_for_internet', 300)
    
    def update_setting(self, section: str, key: str, value: Any):
        """Update a setting and save to file."""
        self.set(section, key, value)
        self.logger.info(f"Updated setting {section}.{key} = {value}")
    
    def get_all_settings(self) -> dict:
        """Get all configuration settings as dictionary."""
        try:
            settings = {}
            for section_name in self.config.sections():
                settings[section_name] = dict(self.config.items(section_name))
            return settings
        except Exception as e:
            self.logger.error(f"Error getting all settings: {str(e)}")
            return {}
    
    def reset_to_defaults(self):
        """Reset configuration to default values."""
        try:
            self.logger.info("Resetting configuration to defaults")
            
            # Remove existing config file
            if self.config_file.exists():
                backup_path = self.config_file.with_suffix('.ini.backup')
                self.config_file.rename(backup_path)
                self.logger.info(f"Backed up existing config to: {backup_path}")
            
            # Create new default configuration
            self.config = ConfigParser()
            self._create_default_config()
            
        except Exception as e:
            self.logger.error(f"Error resetting configuration: {str(e)}")
