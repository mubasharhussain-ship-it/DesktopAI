"""
Automation Executor Module
Executes mouse and keyboard actions based on LLM decisions.
"""

import time
import logging
from typing import Dict, Any, Optional

import pyautogui
import psutil
import win32api
import win32con
import win32gui
import win32process


class AutomationExecutor:
    """Executes automation actions on the desktop."""
    
    def __init__(self):
        """Initialize automation executor."""
        self.logger = logging.getLogger(__name__)
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        pyautogui.PAUSE = 0.1  # Default pause between actions
        
        # Safety settings
        self.max_click_distance = 50  # Max pixels to move in one click
        self.safe_zones = []  # Areas where clicking is restricted
        self.last_action_time = 0
        self.min_action_interval = 0.1  # Minimum seconds between actions
        
    def test_automation(self) -> bool:
        """Test automation capabilities safely."""
        try:
            # Test mouse position
            x, y = pyautogui.position()
            self.logger.info(f"Current mouse position: ({x}, {y})")
            
            # Test screen size
            screen_width, screen_height = pyautogui.size()
            self.logger.info(f"Screen size: {screen_width}x{screen_height}")
            
            # Test safe movement (small movement)
            original_pos = pyautogui.position()
            pyautogui.moveTo(original_pos.x + 1, original_pos.y + 1, duration=0.1)
            pyautogui.moveTo(original_pos.x, original_pos.y, duration=0.1)
            
            self.logger.info("Automation test successful")
            return True
            
        except Exception as e:
            self.logger.error(f"Automation test failed: {str(e)}")
            return False
    
    def execute_action(self, decision: Dict[str, Any]) -> bool:
        """
        Execute an action based on LLM decision.
        
        Args:
            decision: Dictionary containing action details
            
        Returns:
            True if action was executed successfully
        """
        try:
            # Check timing safety
            current_time = time.time()
            if current_time - self.last_action_time < self.min_action_interval:
                time.sleep(self.min_action_interval)
            
            action = decision.get("action", "").lower()
            self.logger.info(f"Executing action: {action}")
            
            success = False
            
            if action == "click":
                success = self._execute_click(decision)
            elif action == "type":
                success = self._execute_type(decision)
            elif action == "key":
                success = self._execute_key(decision)
            elif action == "scroll":
                success = self._execute_scroll(decision)
            elif action == "wait":
                success = self._execute_wait(decision)
            else:
                self.logger.error(f"Unknown action: {action}")
                return False
            
            self.last_action_time = time.time()
            
            if success:
                self.logger.info(f"Action '{action}' executed successfully")
                # Add small delay after successful action
                time.sleep(0.1)
            else:
                self.logger.error(f"Action '{action}' failed")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error executing action: {str(e)}")
            return False
    
    def _execute_click(self, decision: Dict[str, Any]) -> bool:
        """Execute mouse click action."""
        try:
            coordinates = decision.get("coordinates", [])
            if len(coordinates) != 2:
                self.logger.error("Invalid coordinates for click action")
                return False
            
            x, y = int(coordinates[0]), int(coordinates[1])
            
            # Safety checks
            if not self._is_safe_click_position(x, y):
                self.logger.error(f"Click position ({x}, {y}) is not safe")
                return False
            
            # Get click type (default to left click)
            button = decision.get("button", "left").lower()
            clicks = decision.get("clicks", 1)
            
            # Move to position first
            current_pos = pyautogui.position()
            move_duration = min(0.5, max(0.1, 
                abs(x - current_pos.x) + abs(y - current_pos.y)) / 1000)
            
            pyautogui.moveTo(x, y, duration=move_duration)
            
            # Perform click
            if button == "left":
                pyautogui.click(x, y, clicks=clicks, duration=0.1)
            elif button == "right":
                pyautogui.rightClick(x, y)
            elif button == "middle":
                pyautogui.middleClick(x, y)
            else:
                self.logger.error(f"Unknown button type: {button}")
                return False
            
            self.logger.debug(f"Clicked at ({x}, {y}) with {button} button")
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing click: {str(e)}")
            return False
    
    def _execute_type(self, decision: Dict[str, Any]) -> bool:
        """Execute keyboard typing action."""
        try:
            text = decision.get("text", "")
            if not text:
                self.logger.error("No text provided for type action")
                return False
            
            # Safety check for text content
            if not self._is_safe_text(text):
                self.logger.error(f"Text content is not safe: {text[:50]}...")
                return False
            
            # Get typing speed
            interval = decision.get("interval", 0.01)  # Delay between keystrokes
            
            # Type the text
            pyautogui.typewrite(text, interval=interval)
            
            self.logger.debug(f"Typed text: {text[:50]}{'...' if len(text) > 50 else ''}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing type: {str(e)}")
            return False
    
    def _execute_key(self, decision: Dict[str, Any]) -> bool:
        """Execute keyboard key action."""
        try:
            key = decision.get("key", "")
            if not key:
                self.logger.error("No key provided for key action")
                return False
            
            # Safety check for key
            if not self._is_safe_key(key):
                self.logger.error(f"Key is not safe: {key}")
                return False
            
            # Handle key combinations (e.g., "ctrl+c")
            if "+" in key:
                keys = [k.strip() for k in key.split("+")]
                pyautogui.hotkey(*keys)
            else:
                pyautogui.press(key)
            
            self.logger.debug(f"Pressed key: {key}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing key: {str(e)}")
            return False
    
    def _execute_scroll(self, decision: Dict[str, Any]) -> bool:
        """Execute scroll action."""
        try:
            direction = decision.get("direction", "up").lower()
            amount = decision.get("amount", 3)
            
            # Get current mouse position for scroll location
            x, y = pyautogui.position()
            
            if direction in ["up", "down"]:
                scroll_amount = amount if direction == "up" else -amount
                pyautogui.scroll(scroll_amount, x=x, y=y)
            elif direction in ["left", "right"]:
                # Horizontal scrolling (less common)
                pyautogui.hscroll(amount if direction == "right" else -amount, x=x, y=y)
            else:
                self.logger.error(f"Invalid scroll direction: {direction}")
                return False
            
            self.logger.debug(f"Scrolled {direction} by {amount}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing scroll: {str(e)}")
            return False
    
    def _execute_wait(self, decision: Dict[str, Any]) -> bool:
        """Execute wait action."""
        try:
            duration = decision.get("duration", 1.0)
            
            # Safety check for duration
            if duration < 0 or duration > 30:  # Max 30 seconds wait
                self.logger.error(f"Invalid wait duration: {duration}")
                return False
            
            time.sleep(duration)
            
            self.logger.debug(f"Waited for {duration} seconds")
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing wait: {str(e)}")
            return False
    
    def _is_safe_click_position(self, x: int, y: int) -> bool:
        """Check if click position is safe."""
        try:
            # Check screen bounds
            screen_width, screen_height = pyautogui.size()
            if x < 0 or y < 0 or x >= screen_width or y >= screen_height:
                return False
            
            # Check if position is in taskbar (usually bottom 50 pixels on Windows)
            if y >= screen_height - 50:
                return False
            
            # Check safe zones (areas where clicking is restricted)
            for zone in self.safe_zones:
                if (zone["x1"] <= x <= zone["x2"] and 
                    zone["y1"] <= y <= zone["y2"]):
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error checking click safety: {str(e)}")
            return False
    
    def _is_safe_text(self, text: str) -> bool:
        """Check if text is safe to type."""
        # Check for dangerous commands or scripts
        dangerous_patterns = [
            "rm -rf",
            "del /f /s /q",
            "format c:",
            "shutdown",
            "reboot",
            "reg delete",
            "rd /s /q",
            "drop database",
            "drop table"
        ]
        
        text_lower = text.lower()
        for pattern in dangerous_patterns:
            if pattern in text_lower:
                return False
        
        # Check text length (prevent extremely long text)
        if len(text) > 10000:
            return False
        
        return True
    
    def _is_safe_key(self, key: str) -> bool:
        """Check if key combination is safe."""
        # Dangerous key combinations
        dangerous_keys = [
            "alt+f4",  # Close window
            "ctrl+alt+del",  # Task manager
            "win+r",  # Run dialog (potentially dangerous)
            "f10",  # Menu activation in some apps
        ]
        
        key_lower = key.lower()
        for dangerous in dangerous_keys:
            if dangerous == key_lower:
                return False
        
        return True
    
    def get_active_window_info(self) -> Dict[str, Any]:
        """Get information about the currently active window."""
        try:
            # Get active window handle
            hwnd = win32gui.GetForegroundWindow()
            
            # Get window title
            window_title = win32gui.GetWindowText(hwnd)
            
            # Get window rectangle
            rect = win32gui.GetWindowRect(hwnd)
            
            # Get process info
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                process = psutil.Process(pid)
                process_name = process.name()
            except:
                process_name = "Unknown"
            
            return {
                "hwnd": hwnd,
                "title": window_title,
                "rect": rect,
                "process_name": process_name,
                "pid": pid
            }
            
        except Exception as e:
            self.logger.error(f"Error getting window info: {str(e)}")
            return {}
    
    def focus_window(self, window_title: str) -> bool:
        """Focus a window by its title."""
        try:
            hwnd = win32gui.FindWindow(None, window_title)
            if hwnd:
                win32gui.SetForegroundWindow(hwnd)
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error focusing window: {str(e)}")
            return False
    
    def cleanup(self):
        """Cleanup automation executor resources."""
        self.logger.info("Cleaning up automation executor")
        # Reset mouse to a safe position
        try:
            screen_width, screen_height = pyautogui.size()
            pyautogui.moveTo(screen_width // 2, screen_height // 2, duration=0.5)
        except:
            pass
