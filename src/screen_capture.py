"""
Screen Capture Module
Handles screen capture functionality for the desktop agent.
"""

import os
import logging
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Optional

import pyautogui
from PIL import Image
import cv2
import numpy as np


class ScreenCapture:
    """Handles screen capture operations."""
    
    def __init__(self):
        """Initialize screen capture."""
        self.logger = logging.getLogger(__name__)
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
    def test_capture(self) -> bool:
        """Test screen capture functionality."""
        try:
            # Test basic screenshot
            test_path = self.capture_screen()
            if test_path and os.path.exists(test_path):
                self.logger.info("Screen capture test successful")
                # Clean up test screenshot
                try:
                    os.remove(test_path)
                except:
                    pass
                return True
            return False
        except Exception as e:
            self.logger.error(f"Screen capture test failed: {str(e)}")
            return False
    
    def capture_screen(self, region=None) -> Optional[str]:
        """
        Capture the entire screen or a specific region.
        
        Args:
            region: Tuple of (left, top, width, height) for region capture
            
        Returns:
            Path to the saved screenshot file, or None if failed
        """
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"screenshot_{timestamp}.png"
            filepath = self.screenshot_dir / filename
            
            # Capture screenshot
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            
            # Save screenshot
            screenshot.save(str(filepath))
            
            # Verify file was created and has reasonable size
            if filepath.exists() and filepath.stat().st_size > 1000:
                self.logger.debug(f"Screenshot saved: {filepath}")
                return str(filepath)
            else:
                self.logger.error("Screenshot file is too small or doesn't exist")
                return None
                
        except Exception as e:
            self.logger.error(f"Error capturing screen: {str(e)}")
            return None
    
    def capture_window(self, window_title: str) -> Optional[str]:
        """
        Capture a specific window by title.
        
        Args:
            window_title: Title of the window to capture
            
        Returns:
            Path to the saved screenshot file, or None if failed
        """
        try:
            import win32gui
            import win32ui
            import win32con
            
            # Find window
            hwnd = win32gui.FindWindow(None, window_title)
            if not hwnd:
                self.logger.error(f"Window not found: {window_title}")
                return None
            
            # Get window rectangle
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            width = right - left
            height = bottom - top
            
            # Capture the window region
            return self.capture_screen(region=(left, top, width, height))
            
        except ImportError:
            self.logger.warning("win32gui not available, falling back to full screen capture")
            return self.capture_screen()
        except Exception as e:
            self.logger.error(f"Error capturing window: {str(e)}")
            return None
    
    def get_screen_size(self) -> tuple:
        """Get screen size."""
        try:
            return pyautogui.size()
        except Exception as e:
            self.logger.error(f"Error getting screen size: {str(e)}")
            return (1920, 1080)  # Default fallback
    
    def find_image_on_screen(self, template_path: str, confidence=0.8) -> Optional[tuple]:
        """
        Find an image template on the current screen.
        
        Args:
            template_path: Path to the template image
            confidence: Confidence threshold for matching (0.0 to 1.0)
            
        Returns:
            (x, y) coordinates of the center of the found image, or None
        """
        try:
            location = pyautogui.locateOnScreen(template_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                return (center.x, center.y)
            return None
        except Exception as e:
            self.logger.error(f"Error finding image on screen: {str(e)}")
            return None
    
    def find_text_on_screen(self, text: str) -> list:
        """
        Find text on the current screen using OCR.
        
        Args:
            text: Text to find
            
        Returns:
            List of (x, y) coordinates where text was found
        """
        try:
            # This would require OCR functionality
            # For now, return empty list as OCR is complex and not in core requirements
            self.logger.warning("Text finding not implemented - requires OCR")
            return []
        except Exception as e:
            self.logger.error(f"Error finding text on screen: {str(e)}")
            return []
    
    def get_pixel_color(self, x: int, y: int) -> tuple:
        """
        Get the RGB color of a pixel at the given coordinates.
        
        Args:
            x, y: Pixel coordinates
            
        Returns:
            (R, G, B) tuple
        """
        try:
            return pyautogui.pixel(x, y)
        except Exception as e:
            self.logger.error(f"Error getting pixel color: {str(e)}")
            return (0, 0, 0)
    
    def cleanup_screenshots(self, keep_last_n=10):
        """
        Clean up old screenshot files, keeping only the most recent ones.
        
        Args:
            keep_last_n: Number of recent screenshots to keep
        """
        try:
            # Get all screenshot files
            screenshot_files = list(self.screenshot_dir.glob("screenshot_*.png"))
            
            if len(screenshot_files) <= keep_last_n:
                return
            
            # Sort by modification time (newest first)
            screenshot_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remove old files
            for filepath in screenshot_files[keep_last_n:]:
                try:
                    filepath.unlink()
                    self.logger.debug(f"Removed old screenshot: {filepath}")
                except Exception as e:
                    self.logger.warning(f"Failed to remove {filepath}: {str(e)}")
                    
        except Exception as e:
            self.logger.error(f"Error cleaning up screenshots: {str(e)}")
    
    def capture_screen_with_annotations(self, annotations: list) -> Optional[str]:
        """
        Capture screen and add annotations (rectangles, circles, text).
        
        Args:
            annotations: List of annotation dictionaries
            
        Returns:
            Path to annotated screenshot file
        """
        try:
            # Capture base screenshot
            base_path = self.capture_screen()
            if not base_path:
                return None
            
            # Load image with OpenCV
            image = cv2.imread(base_path)
            if image is None:
                return None
            
            # Add annotations
            for annotation in annotations:
                ann_type = annotation.get("type", "")
                
                if ann_type == "rectangle":
                    x, y, w, h = annotation.get("coords", [0, 0, 100, 100])
                    color = annotation.get("color", (0, 255, 0))
                    thickness = annotation.get("thickness", 2)
                    cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
                
                elif ann_type == "circle":
                    x, y = annotation.get("center", [100, 100])
                    radius = annotation.get("radius", 20)
                    color = annotation.get("color", (0, 255, 0))
                    thickness = annotation.get("thickness", 2)
                    cv2.circle(image, (x, y), radius, color, thickness)
                
                elif ann_type == "text":
                    x, y = annotation.get("position", [10, 30])
                    text = annotation.get("text", "")
                    color = annotation.get("color", (0, 255, 0))
                    font_scale = annotation.get("font_scale", 1.0)
                    cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                               font_scale, color, 2, cv2.LINE_AA)
            
            # Save annotated image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            annotated_filename = f"annotated_{timestamp}.png"
            annotated_path = self.screenshot_dir / annotated_filename
            
            cv2.imwrite(str(annotated_path), image)
            
            # Remove original screenshot
            try:
                os.remove(base_path)
            except:
                pass
            
            return str(annotated_path)
            
        except Exception as e:
            self.logger.error(f"Error creating annotated screenshot: {str(e)}")
            return None
    
    def cleanup(self):
        """Cleanup screen capture resources."""
        self.logger.info("Cleaning up screen capture")
        # Clean up old screenshots
        self.cleanup_screenshots(keep_last_n=5)
