# 📋 How to Copy This Desktop AI to Another PC

This guide shows you how to easily transfer the Desktop AI Assistant to a new Windows computer.

## Method 1: Simple Folder Copy (Recommended)

### 1. Package the Folder
On your current PC:
- Copy the entire Desktop AI folder (with all subfolders)
- You can zip it for easier transfer: Right-click folder → "Send to" → "Compressed folder"

### 2. Transfer to New PC
- Copy the folder to the new PC (via USB drive, network, cloud storage, etc.)
- Place it wherever you want (example: `C:\DesktopAI\`)

### 3. Run Setup on New PC
Open Command Prompt as Administrator:
```bash
cd C:\DesktopAI
python setup.py
```

The setup will:
- ✅ Install all Python dependencies
- ✅ Download the AI model (Ollama + LLaVA)
- ✅ Create necessary folders
- ✅ Test everything works

### 4. Start Using
```bash
python main.py
```

## Method 2: Fresh Installation

If you want to install fresh on the new PC:

### 1. Install Python
- Download Python 3.8+ from python.org
- ✅ Check "Add Python to PATH" during installation

### 2. Install Ollama
- Visit https://ollama.com/
- Download and install Ollama for Windows
- Open Command Prompt and run: `ollama pull llava`

### 3. Copy Project Files
- Copy just the project files (no need for Python packages)
- Run `python setup.py` to install dependencies

## 📁 What Gets Copied

### Essential Files (Always Copy These):
```
📁 DesktopAI/
├── 📄 main.py                 # Main application
├── 📄 setup.py               # Setup script
├── 📄 README.md              # This guide
├── 📁 src/                   # Core application code
│   ├── automation_executor.py
│   ├── command_processor.py
│   ├── config_manager.py
│   ├── llm_interface.py
│   ├── screen_capture.py
│   └── utils.py
├── 📁 config/                # Configuration files
│   └── settings.ini
├── 📁 data/                  # Command and rules files
│   ├── commands.txt
│   └── rules.txt
└── 📁 logs/                  # Log files (optional to copy)
```

### Generated Folders (Created Automatically):
- `screenshots/` - Temporary screenshot storage
- `logs/` - Application logs

## 🔧 Troubleshooting

### "Python not found"
- Install Python from python.org
- Make sure to check "Add Python to PATH"

### "Ollama not found" 
- Install Ollama from ollama.com
- Run `ollama pull llava` after installation

### Permission Errors
- Run Command Prompt as Administrator
- Make sure you have write permissions in the folder

### Dependencies Missing
- Run `python setup.py` again
- Check internet connection for downloads

## 💡 Pro Tips

### For Multiple PCs:
1. Set up once on your main PC
2. Test that everything works
3. Copy the entire folder to other PCs
4. Run `python setup.py` on each new PC

### Keep It Updated:
- The AI model is stored locally in Ollama
- Your commands and rules are in the `data/` folder
- Configuration settings are in `config/settings.ini`

### Backup Your Setup:
- Copy your customized `data/commands.txt` and `data/rules.txt`
- Copy your `config/settings.ini` if you made changes
- These contain your personal automation preferences

## 📞 Need Help?

If you run into issues:
1. Check the logs in `logs/app.log`
2. Run `python setup.py` again
3. Make sure you're running as Administrator
4. Verify Python and Ollama are installed correctly