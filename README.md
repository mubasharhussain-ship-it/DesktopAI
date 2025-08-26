# Windows Desktop AI Assistant

An intelligent desktop automation system that uses a local Large Language Model (LLM) to understand what's on your screen and control your computer with natural language commands. The AI can open apps, browse the web, type text, click buttons, and perform complex tasks - all running completely offline on your computer.

## ✨ Key Features

- **🧠 Smart Visual Understanding**: AI analyzes your desktop screenshots to understand what's currently on screen
- **🗣️ Natural Language Control**: Give commands in plain English like "open notepad and type hello world"
- **🔒 Completely Offline**: Runs locally using Ollama - no internet required after setup
- **⚡ Mouse & Keyboard Automation**: AI decides exactly where to click and what to type
- **🛡️ Safety First**: Built-in safety rules prevent harmful actions
- **📁 Portable**: Everything in one folder - easy to copy to any Windows PC
- **📝 File-Based Commands**: Write commands in a text file, AI reads and executes them
- **🌐 Smart Internet Handling**: Waits for internet when opening apps that need it

## 🖥️ System Requirements

- **Windows 10/11** (64-bit)
- **Python 3.8+** 
- **8GB+ RAM** (for AI model)
- **5GB+ free disk space** (for AI models)
- **Admin privileges** (recommended)

## 🚀 Setup Instructions

### Step 1: Copy to Your PC
1. Download/copy this entire folder to your Windows computer
2. Place it anywhere you want (like `C:\DesktopAI\`)

### Step 2: Install Requirements
Open Command Prompt as Administrator and run:

```bash
# Navigate to the project folder
cd C:\DesktopAI

# Run the automated setup
python setup.py
```

### Step 3: Install Ollama (AI Engine)
The setup script will guide you, but here's the manual process:

1. **Download Ollama**: Visit https://ollama.com/
2. **Install**: Run the installer for Windows
3. **Download AI Model**: Open Command Prompt and run:
   ```bash
   ollama pull llava
   ```

### Step 4: Start the AI Assistant
```bash
python main.py
```

## 📝 How to Use

### 1. Add Commands
Edit the `data/commands.txt` file and add your commands:
```
open notepad
type Hello, this is my AI assistant!
save the file as test.txt
```

### 2. The AI Will:
- 📸 Take a screenshot of your desktop
- 🔍 Analyze what's visible on screen
- 🤖 Decide exactly where to click and what to type
- ⚡ Execute the actions automatically

### 3. Watch the Magic
The AI will:
- Open Notepad by finding and clicking it
- Type your text exactly where the cursor is
- Navigate menus to save the file
- Handle dialog boxes and interactions

## 🌐 Internet Connectivity Features

The AI automatically handles internet requirements:

### Apps That Need Internet:
- **Browsers**: Chrome, Firefox, Edge
- **Communication**: Outlook, Teams, Discord, Skype
- **Entertainment**: Steam, Spotify, YouTube
- **Cloud Services**: OneDrive, Google Drive, Dropbox

### What Happens:
1. AI detects when you want to open an internet-dependent app
2. Checks if internet is available
3. If no internet: **Waits and retries** until connection is restored
4. Shows status messages about connectivity
5. Continues with offline tasks while waiting

### Example:
```
# Command: open chrome and go to google.com
# AI Response: "Checking internet connectivity..."
# If offline: "Waiting for internet connection..."
# When online: "Internet restored, opening Chrome..."
```

## ⚙️ Configuration

### Settings File: `config/settings.ini`
```ini
[AUTOMATION]
command_delay = 2.0        # Seconds between commands
polling_interval = 1.0     # How often to check for new commands
failsafe = true           # Enable emergency stop (move mouse to corner)

[SAFETY]
safe_mode = true          # Enable all safety checks
max_click_distance = 50   # Maximum pixel distance for clicks

[LLM]
model = llava             # AI model to use
temperature = 0.1         # AI creativity (0.0 = precise, 1.0 = creative)
```

### Rules File: `data/rules.txt`
Customize the AI's behavior and safety rules. Add your own rules like:
```
18. Never close important applications without confirmation
19. Always double-check file paths before saving
20. Prioritize user productivity and safety
```

## 🛡️ Safety Features

### Built-in Protections:
- ❌ **No destructive actions** (deleting files, formatting drives)
- 🔒 **No password access** or sensitive information handling
- ⏱️ **Rate limiting** to prevent runaway automation
- 🚨 **Emergency stop** - move mouse to screen corner to abort
- 📝 **Full logging** of all actions and decisions

### Safe Actions Only:
- ✅ Opening applications
- ✅ Typing text in visible fields
- ✅ Clicking buttons and menus
- ✅ Navigating interfaces
- ✅ File operations (create, save, open)

## 📂 Project Structure

```
📁 DesktopAI/
├── 📄 main.py              # Main application entry point
├── 📄 setup.py             # Automated setup script
├── 📄 README.md            # This guide
├── 📄 COPY_TO_NEW_PC.md    # Transfer instructions
├── 📁 src/                 # Core application code
│   ├── llm_interface.py    # AI communication
│   ├── screen_capture.py   # Screenshot handling
│   ├── automation_executor.py # Mouse/keyboard control
│   ├── command_processor.py   # Command file reading
│   ├── config_manager.py   # Settings management
│   └── utils.py           # Utility functions
├── 📁 config/             # Configuration files
│   └── settings.ini       # Main settings
├── 📁 data/               # User data
│   ├── commands.txt       # Your commands go here
│   ├── rules.txt          # AI behavior rules
│   └── processed_commands.txt # Command history
├── 📁 logs/               # Application logs
├── 📁 screenshots/        # Temporary screenshots (auto-cleaned)
```

## 🚀 Advanced Usage

### Batch Commands
Add multiple commands for complex workflows:
```
open file explorer
navigate to documents folder
create new folder called "AI Projects"
open notepad
type Project notes and ideas
save as notes.txt in AI Projects folder
close notepad
```

### Conditional Commands
The AI understands context:
```
if calculator is open then calculate 15 plus 27
otherwise open calculator first
```

### App-Specific Commands
```
in chrome: go to gmail.com and check inbox
in word: create new document and set font to Arial 12pt
in excel: open budget.xlsx and sum column B
```

## 📞 Troubleshooting

### Common Issues:

**"Python not found"**
- Install Python from python.org
- Check "Add Python to PATH" during installation

**"Ollama not accessible"**
- Install Ollama from ollama.com
- Run `ollama pull llava` in Command Prompt

**"Permission denied"**
- Run Command Prompt as Administrator
- Ensure antivirus isn't blocking the application

**"AI not responding"**
- Check `logs/app.log` for errors
- Restart with `python main.py`
- Verify Ollama is running: `ollama list`

### Getting Help:
1. Check the log files in `logs/app.log`
2. Verify all requirements are installed
3. Test with simple commands first
4. Make sure you have admin privileges

## 🎯 Example Workflows

### Daily Productivity:
```
open outlook and check for new emails
open chrome and go to calendar.google.com
open notepad for daily notes
minimize all windows except notepad
```

### Development Setup:
```
open visual studio code
open file explorer to projects folder
open chrome and navigate to github.com
arrange windows side by side
```

### Content Creation:
```
open obs studio for recording
open chrome and go to youtube.com
position windows for screen recording
start recording when ready
```

## 🔄 Copying to Another PC

See the detailed guide in `COPY_TO_NEW_PC.md` for step-by-step instructions on transferring this entire setup to a new computer. It's designed to be completely portable!
