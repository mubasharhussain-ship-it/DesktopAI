#!/usr/bin/env python3
"""
Setup script for Desktop Automation Agent
Handles installation and configuration of the application.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path


def setup_logging():
    """Setup basic logging for setup process."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)


def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python {sys.version}")
    return True


def install_requirements():
    """Install required Python packages."""
    logger = logging.getLogger(__name__)
    
    requirements = [
        "pyautogui>=0.9.54",
        "Pillow>=8.0.0",
        "opencv-python>=4.5.0",
        "psutil>=5.8.0",
        "requests>=2.25.0",
        "pywin32>=227; sys_platform=='win32'",
        "configparser>=5.0.0"
    ]
    
    logger.info("Installing Python dependencies...")
    
    for requirement in requirements:
        try:
            logger.info(f"Installing {requirement}")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", requirement
            ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            logger.info(f"✓ {requirement} installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"✗ Failed to install {requirement}: {e}")
            return False
    
    logger.info("All Python dependencies installed successfully")
    return True


def check_ollama_installation():
    """Check if Ollama is installed and accessible."""
    logger = logging.getLogger(__name__)
    
    try:
        result = subprocess.run(
            ["ollama", "version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            logger.info(f"✓ Ollama is installed: {result.stdout.strip()}")
            return True
        else:
            logger.warning("Ollama command failed")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        logger.warning("✗ Ollama not found or not accessible")
        return False


def install_ollama():
    """Provide instructions for Ollama installation."""
    logger = logging.getLogger(__name__)
    
    logger.info("Ollama is required for local LLM functionality")
    logger.info("Please install Ollama manually:")
    logger.info("1. Visit https://ollama.com/")
    logger.info("2. Download and install Ollama for Windows")
    logger.info("3. After installation, run: ollama pull llava")
    logger.info("4. Then run this setup script again")
    
    return False


def setup_ollama_model():
    """Setup the default LLM model."""
    logger = logging.getLogger(__name__)
    
    model_name = "llava"
    logger.info(f"Setting up LLM model: {model_name}")
    
    try:
        # Check if model is already available
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if model_name in result.stdout:
            logger.info(f"✓ Model {model_name} is already available")
            return True
        
        # Pull the model
        logger.info(f"Downloading model {model_name} (this may take a while)...")
        result = subprocess.run(
            ["ollama", "pull", model_name],
            capture_output=True,
            text=True,
            timeout=1800  # 30 minutes timeout
        )
        
        if result.returncode == 0:
            logger.info(f"✓ Model {model_name} downloaded successfully")
            return True
        else:
            logger.error(f"✗ Failed to download model: {result.stderr}")
            return False
    
    except subprocess.TimeoutExpired:
        logger.error("Model download timed out (30 minutes)")
        return False
    except Exception as e:
        logger.error(f"Error setting up model: {str(e)}")
        return False


def create_directory_structure():
    """Create necessary directories."""
    logger = logging.getLogger(__name__)
    
    directories = [
        "config",
        "data", 
        "logs",
        "screenshots",
        "src"
    ]
    
    logger.info("Creating directory structure...")
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            logger.info(f"✓ Created directory: {directory}")
        except Exception as e:
            logger.error(f"✗ Failed to create directory {directory}: {str(e)}")
            return False
    
    return True


def create_default_files():
    """Create default configuration and data files."""
    logger = logging.getLogger(__name__)
    
    logger.info("Creating default configuration files...")
    
    # This would typically initialize the config files
    # The actual files are created by the application modules
    # when they run for the first time
    
    try:
        # Import the application modules to trigger file creation
        sys.path.insert(0, 'src')
        from config_manager import ConfigManager
        from command_processor import CommandProcessor
        
        # Initialize to create default files
        config = ConfigManager()
        cmd_processor = CommandProcessor()
        
        logger.info("✓ Default configuration files created")
        return True
        
    except Exception as e:
        logger.error(f"✗ Failed to create default files: {str(e)}")
        return False


def test_installation():
    """Test the installation by running basic functionality."""
    logger = logging.getLogger(__name__)
    
    logger.info("Testing installation...")
    
    try:
        # Test imports
        import pyautogui
        from PIL import Image
        import cv2
        import psutil
        import requests
        
        # Test screen capture
        screenshot = pyautogui.screenshot()
        logger.info("✓ Screen capture test passed")
        
        # Test Ollama connectivity
        import subprocess
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            logger.info("✓ Ollama connectivity test passed")
        else:
            logger.warning("⚠ Ollama connectivity test failed")
        
        logger.info("✓ Installation test completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"✗ Installation test failed: {str(e)}")
        return False


def main():
    """Main setup function."""
    logger = setup_logging()
    
    print("=" * 60)
    print("Desktop Automation Agent Setup")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Create directory structure
    if not create_directory_structure():
        logger.error("Failed to create directory structure")
        return 1
    
    # Install Python requirements
    if not install_requirements():
        logger.error("Failed to install Python requirements")
        return 1
    
    # Check Ollama installation
    if not check_ollama_installation():
        install_ollama()
        return 1
    
    # Setup LLM model
    if not setup_ollama_model():
        logger.error("Failed to setup LLM model")
        return 1
    
    # Create default files
    if not create_default_files():
        logger.error("Failed to create default files")
        return 1
    
    # Test installation
    if not test_installation():
        logger.warning("Installation test failed - manual testing recommended")
    
    print("\n" + "=" * 60)
    print("Setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Edit 'data/commands.txt' to add your automation commands")
    print("2. Review 'config/settings.ini' to adjust settings if needed")
    print("3. Run 'python main.py' to start the automation agent")
    print("\nFor help and documentation, see README.md")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
