"""
Command Processor Module
Handles reading and processing user commands from file.
"""

import os
import time
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime


class CommandProcessor:
    """Processes user commands from file input."""
    
    def __init__(self):
        """Initialize command processor."""
        self.logger = logging.getLogger(__name__)
        self.commands_file = Path("data/commands.txt")
        self.processed_commands_file = Path("data/processed_commands.txt")
        self.last_modified = 0
        self.processed_commands = set()
        
        # Create commands file if it doesn't exist
        self.commands_file.parent.mkdir(exist_ok=True)
        if not self.commands_file.exists():
            self._create_default_commands_file()
        
        # Load previously processed commands
        self._load_processed_commands()
    
    def _create_default_commands_file(self):
        """Create default commands file with examples."""
        default_content = """# Desktop Automation Commands
# Add your commands here, one per line
# Lines starting with # are comments and will be ignored
# Examples:
# open notepad
# type hello world
# press enter
# click on file menu
# close window

# Your commands:
"""
        try:
            with open(self.commands_file, 'w', encoding='utf-8') as f:
                f.write(default_content)
            self.logger.info(f"Created default commands file: {self.commands_file}")
        except Exception as e:
            self.logger.error(f"Error creating commands file: {str(e)}")
    
    def _load_processed_commands(self):
        """Load previously processed commands to avoid duplicates."""
        try:
            if self.processed_commands_file.exists():
                with open(self.processed_commands_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            self.processed_commands.add(line)
                self.logger.debug(f"Loaded {len(self.processed_commands)} processed commands")
        except Exception as e:
            self.logger.error(f"Error loading processed commands: {str(e)}")
    
    def get_pending_commands(self) -> List[str]:
        """Get list of pending commands from file."""
        try:
            # Check if file exists
            if not self.commands_file.exists():
                return []
            
            # Check if file has been modified
            current_modified = self.commands_file.stat().st_mtime
            if current_modified == self.last_modified:
                return []
            
            self.last_modified = current_modified
            
            # Read commands from file
            commands = []
            with open(self.commands_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Skip already processed commands
                    if line in self.processed_commands:
                        continue
                    
                    # Validate command
                    if self._is_valid_command(line):
                        commands.append(line)
                    else:
                        self.logger.warning(f"Invalid command at line {line_num}: {line}")
            
            if commands:
                self.logger.info(f"Found {len(commands)} new commands")
            
            return commands
            
        except Exception as e:
            self.logger.error(f"Error reading commands: {str(e)}")
            return []
    
    def _is_valid_command(self, command: str) -> bool:
        """Validate if a command is properly formatted and safe."""
        try:
            # Check command length
            if len(command) > 500:
                return False
            
            # Check for dangerous commands
            dangerous_patterns = [
                "rm -rf",
                "del /f /s /q",
                "format c:",
                "shutdown /s",
                "reboot",
                "reg delete",
                "rd /s /q",
                "drop database",
                "drop table",
                "kill -9",
                "taskkill /f"
            ]
            
            command_lower = command.lower()
            for pattern in dangerous_patterns:
                if pattern in command_lower:
                    self.logger.warning(f"Dangerous command detected: {command}")
                    return False
            
            # Basic format validation
            # Commands should be natural language instructions
            if len(command.split()) < 2:
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating command: {str(e)}")
            return False
    
    def mark_command_processed(self, command: str):
        """Mark a command as processed."""
        try:
            self.processed_commands.add(command)
            
            # Append to processed commands file
            with open(self.processed_commands_file, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"# Processed at {timestamp}\n{command}\n")
            
            self.logger.debug(f"Marked command as processed: {command}")
            
        except Exception as e:
            self.logger.error(f"Error marking command as processed: {str(e)}")
    
    def clear_processed_commands(self):
        """Clear the list of processed commands."""
        try:
            self.processed_commands.clear()
            
            # Archive current processed commands file
            if self.processed_commands_file.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_path = self.processed_commands_file.parent / f"processed_commands_archive_{timestamp}.txt"
                self.processed_commands_file.rename(archive_path)
                self.logger.info(f"Archived processed commands to: {archive_path}")
            
            self.logger.info("Cleared processed commands list")
            
        except Exception as e:
            self.logger.error(f"Error clearing processed commands: {str(e)}")
    
    def get_command_history(self, limit: int = 100) -> List[dict]:
        """Get command history with timestamps."""
        try:
            history = []
            
            if not self.processed_commands_file.exists():
                return history
            
            with open(self.processed_commands_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            current_timestamp = None
            for line in lines:
                line = line.strip()
                
                if line.startswith('# Processed at '):
                    # Extract timestamp
                    timestamp_str = line.replace('# Processed at ', '')
                    try:
                        current_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                    except:
                        current_timestamp = None
                elif line and not line.startswith('#'):
                    # This is a command
                    history.append({
                        'command': line,
                        'timestamp': current_timestamp,
                        'timestamp_str': current_timestamp.strftime("%Y-%m-%d %H:%M:%S") if current_timestamp else "Unknown"
                    })
            
            # Return most recent commands first
            return list(reversed(history))[-limit:]
            
        except Exception as e:
            self.logger.error(f"Error getting command history: {str(e)}")
            return []
    
    def add_command(self, command: str):
        """Add a command to the commands file."""
        try:
            if not self._is_valid_command(command):
                self.logger.error(f"Invalid command: {command}")
                return False
            
            with open(self.commands_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{command}\n")
            
            self.logger.info(f"Added command: {command}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding command: {str(e)}")
            return False
    
    def remove_command(self, command: str):
        """Remove a command from the commands file."""
        try:
            if not self.commands_file.exists():
                return False
            
            # Read all lines
            with open(self.commands_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Filter out the command to remove
            filtered_lines = []
            removed = False
            
            for line in lines:
                if line.strip() == command:
                    removed = True
                    continue
                filtered_lines.append(line)
            
            if removed:
                # Write back the filtered content
                with open(self.commands_file, 'w', encoding='utf-8') as f:
                    f.writelines(filtered_lines)
                
                self.logger.info(f"Removed command: {command}")
                return True
            else:
                self.logger.warning(f"Command not found for removal: {command}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error removing command: {str(e)}")
            return False
    
    def get_file_status(self) -> dict:
        """Get status information about command files."""
        try:
            status = {
                'commands_file_exists': self.commands_file.exists(),
                'processed_file_exists': self.processed_commands_file.exists(),
                'commands_file_size': 0,
                'processed_file_size': 0,
                'last_modified': None,
                'total_processed': len(self.processed_commands)
            }
            
            if status['commands_file_exists']:
                stat = self.commands_file.stat()
                status['commands_file_size'] = stat.st_size
                status['last_modified'] = datetime.fromtimestamp(stat.st_mtime)
            
            if status['processed_file_exists']:
                status['processed_file_size'] = self.processed_commands_file.stat().st_size
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting file status: {str(e)}")
            return {}
