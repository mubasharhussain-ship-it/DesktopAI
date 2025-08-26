#!/usr/bin/env python3
"""
Offline LLM-Powered Desktop Automation Agent
Main entry point for the desktop automation system.
"""

import os
import sys
import time
import logging
import signal
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config_manager import ConfigManager
from llm_interface import LLMInterface
from screen_capture import ScreenCapture
from automation_executor import AutomationExecutor
from command_processor import CommandProcessor
from utils import setup_logging, check_internet_connection, wait_for_internet


class DesktopAgent:
    """Main desktop automation agent class."""
    
    def __init__(self):
        """Initialize the desktop agent."""
        self.config = ConfigManager()
        self.logger = setup_logging()
        self.running = False
        
        # Initialize components
        self.screen_capture = ScreenCapture()
        self.llm_interface = LLMInterface(self.config)
        self.automation_executor = AutomationExecutor()
        self.command_processor = CommandProcessor()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
    
    def initialize(self):
        """Initialize all components and check prerequisites."""
        self.logger.info("Initializing Desktop Automation Agent...")
        
        # Check if internet is available for initial Ollama setup
        if not check_internet_connection():
            self.logger.warning("No internet connection detected. Waiting for connection...")
            wait_for_internet(timeout=60)
        
        # Initialize LLM interface
        if not self.llm_interface.initialize():
            self.logger.error("Failed to initialize LLM interface")
            return False
        
        # Test screen capture
        if not self.screen_capture.test_capture():
            self.logger.error("Failed to initialize screen capture")
            return False
        
        # Test automation capabilities
        if not self.automation_executor.test_automation():
            self.logger.error("Failed to initialize automation executor")
            return False
        
        self.logger.info("All components initialized successfully")
        return True
    
    def process_command(self, command):
        """Process a single user command."""
        try:
            self.logger.info(f"Processing command: {command}")
            
            # Capture current screen
            screenshot_path = self.screen_capture.capture_screen()
            if not screenshot_path:
                self.logger.error("Failed to capture screen")
                return False
            
            # Get LLM decision
            decision = self.llm_interface.analyze_screen_and_command(
                screenshot_path, command
            )
            
            if not decision:
                self.logger.error("Failed to get LLM decision")
                return False
            
            # Execute the decision
            success = self.automation_executor.execute_action(decision)
            
            if success:
                self.logger.info(f"Successfully executed action: {decision.get('action', 'unknown')}")
            else:
                self.logger.error(f"Failed to execute action: {decision.get('action', 'unknown')}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"Error processing command '{command}': {str(e)}")
            return False
    
    def run(self):
        """Main execution loop."""
        self.logger.info("Starting Desktop Automation Agent...")
        self.running = True
        
        # Initialize components
        if not self.initialize():
            self.logger.error("Failed to initialize agent")
            return
        
        self.logger.info("Agent is ready and waiting for commands...")
        
        # Main processing loop
        while self.running:
            try:
                # Check for new commands
                commands = self.command_processor.get_pending_commands()
                
                for command in commands:
                    if not self.running:
                        break
                    
                    # Process each command
                    self.process_command(command)
                    
                    # Mark command as processed
                    self.command_processor.mark_command_processed(command)
                    
                    # Add delay between commands for safety
                    time.sleep(self.config.get_command_delay())
                
                # Sleep before checking for new commands
                time.sleep(self.config.get_polling_interval())
                
            except KeyboardInterrupt:
                self.logger.info("Received keyboard interrupt")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error in main loop: {str(e)}")
                time.sleep(5)  # Wait before retrying
        
        self.logger.info("Desktop Automation Agent stopped")
    
    def shutdown(self):
        """Gracefully shutdown all components."""
        self.logger.info("Shutting down Desktop Automation Agent...")
        self.running = False
        
        # Cleanup components
        if hasattr(self, 'screen_capture'):
            self.screen_capture.cleanup()
        
        if hasattr(self, 'llm_interface'):
            self.llm_interface.cleanup()
        
        if hasattr(self, 'automation_executor'):
            self.automation_executor.cleanup()
        
        self.logger.info("Shutdown complete")


def main():
    """Main entry point."""
    try:
        # Create agent instance
        agent = DesktopAgent()
        
        # Run the agent
        agent.run()
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)
    finally:
        # Ensure cleanup
        if 'agent' in locals():
            agent.shutdown()


if __name__ == "__main__":
    main()
