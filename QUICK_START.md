# 🚀 Quick Start Guide

Get your AI Desktop Assistant running in 5 minutes!

## Step 1: Copy This Folder
- Copy the entire `DesktopAI` folder to your Windows PC
- Place it somewhere like `C:\DesktopAI\`

## Step 2: One-Click Setup
**Easy Way**: Double-click `INSTALL.bat`

**Manual Way**: 
```bash
cd C:\DesktopAI
python setup.py
```

## Step 3: Install Ollama (if prompted)
1. Go to https://ollama.com/
2. Download and install Ollama for Windows
3. Open Command Prompt and run: `ollama pull llava`

## Step 4: Start the AI
**Easy Way**: Double-click `START.bat`

**Manual Way**: `python main.py`

## Step 5: Add Your Commands
Edit `data\commands.txt` and add:
```
open notepad
type Hello World!
save as test.txt
```

## That's It! 🎉
The AI will now:
- Take screenshots of your desktop
- Understand what's on screen
- Execute your commands automatically
- Handle mouse clicks and keyboard typing

## Emergency Stop
Move your mouse to any screen corner to stop immediately!

## Need Help?
- Check `logs\app.log` for detailed information
- See `README.md` for complete documentation
- See `COPY_TO_NEW_PC.md` for transfer instructions