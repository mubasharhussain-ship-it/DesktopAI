# Overview

**COMPLETED PROJECT**: Windows Desktop AI Assistant - A complete, portable Windows desktop automation system that uses local Large Language Models (LLM) to understand screen content and execute user commands through mouse and keyboard automation.

## Key Features Implemented:
- ✅ **Local LLM Integration**: Uses Ollama with LLaVA model for complete offline operation
- ✅ **Visual Screen Understanding**: AI analyzes desktop screenshots to understand current state
- ✅ **Natural Language Commands**: File-based command system - user writes commands in plain English
- ✅ **Smart Mouse & Keyboard Control**: AI determines exact coordinates and keystrokes needed
- ✅ **Internet Connectivity Handling**: Automatically waits for internet when apps require it
- ✅ **Safety Mechanisms**: Built-in safety rules prevent harmful automation
- ✅ **Portable Design**: Complete folder structure for easy copying between PCs
- ✅ **Comprehensive Logging**: Detailed logging of all actions and decisions
- ✅ **Easy Setup**: Automated setup script and batch files for one-click operation

## Current Status: READY FOR DEPLOYMENT
The system is fully functional and includes:
- Complete source code with all modules
- Automated setup and installation scripts
- Comprehensive documentation and user guides
- Safety rules and configuration system
- Easy transfer instructions for copying to new PCs

# User Preferences

Preferred communication style: Simple, everyday language.
Target Platform: Windows 10/11 desktop environments
Use Case: Completely offline desktop automation with file-based command input

# System Architecture

## Core Components Architecture

The application follows a modular architecture with clear separation of concerns:

**Main Controller (`main.py`)**: Central orchestrator that initializes and coordinates all components, handles graceful shutdown through signal handlers, and manages the main execution loop.

**Configuration Management (`config_manager.py`)**: Centralized configuration system using INI files to manage LLM settings, automation parameters, logging preferences, and safety configurations. Creates default configurations automatically when none exist.

**LLM Interface (`llm_interface.py`)**: Handles communication with Ollama for local LLM inference, manages model selection and parameters, processes vision-language tasks for screen understanding, and enforces automation safety rules through prompt engineering.

**Screen Capture (`screen_capture.py`)**: Manages desktop screenshot functionality using PyAutoGUI and PIL, provides image preprocessing with OpenCV, supports region-specific captures, and includes automatic cleanup of temporary files.

**Automation Executor (`automation_executor.py`)**: Executes mouse and keyboard actions based on LLM decisions, implements safety mechanisms including fail-safe triggers and movement restrictions, manages action timing and coordination, and provides comprehensive action logging.

**Command Processor (`command_processor.py`)**: Handles file-based command input system, processes natural language commands from text files, tracks processed commands to avoid duplication, and manages command history and state.

## Data Flow Architecture

Commands flow from text file input through the command processor, which triggers screen capture for current state analysis. The captured screenshot is sent to the LLM interface along with the command and safety rules. The LLM analyzes the visual content and returns structured JSON responses containing specific actions and coordinates. The automation executor validates and executes these actions while enforcing safety constraints.

## Safety and Security Design

The system implements multiple layers of safety including hardcoded safety rules in the LLM prompt, coordinate validation and movement restrictions, fail-safe mechanisms (mouse corner abort), action rate limiting and timing controls, and comprehensive logging of all actions and decisions.

## File-based Communication

The application uses a file-based approach for user interaction, monitoring `data/commands.txt` for new commands, maintaining processed command history, and providing example command formats in the default file structure.

## Logging and Monitoring

Comprehensive logging system with rotating file handlers, separate log files for different components, configurable log levels and formats, and automatic log cleanup and archiving.

# External Dependencies

## Core Python Libraries
- **PyAutoGUI**: Mouse and keyboard automation, screen capture functionality
- **Pillow (PIL)**: Image processing and manipulation for screenshots
- **OpenCV (cv2)**: Advanced image processing and computer vision operations
- **Requests**: HTTP communication with Ollama API
- **PSUtil**: System process monitoring and management
- **PyWin32**: Windows-specific API access for enhanced automation (Windows only)

## Local LLM Infrastructure
- **Ollama**: Local LLM inference server running on localhost:11434
- **LLaVA Model**: Default vision-language model for screen understanding and command interpretation
- **Local Model Storage**: Requires 5GB+ disk space for model files

## Operating System Dependencies
- **Windows 10/11**: Primary target platform with specific API integrations
- **Administrative Privileges**: Recommended for full automation capabilities
- **System Resources**: 8GB+ RAM for optimal LLM inference performance

## File System Dependencies
- **Configuration Files**: INI-based configuration in `config/` directory
- **Data Files**: Command input and rules stored in `data/` directory
- **Logging System**: Rotating log files in `logs/` directory
- **Screenshot Storage**: Temporary screenshot storage in `screenshots/` directory

## Network Dependencies
- **Localhost Communication**: HTTP communication with local Ollama server
- **No Internet Required**: Fully offline operation after initial setup and model download