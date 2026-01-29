# 🛠️ Shipra AI - Troubleshooting & Error Guide

This document contains solutions for the specific errors encountered during the development of Shipra AI, particularly on **Python 3.11+**.

---

## 1. 🐍 Python 3.11 & Whisper Issues

### 🔴 `ModuleNotFoundError: No module named 'whisper'` or `AttributeError: module 'whisper' has no attribute 'load_model'`
**Context**: This happens often on Python 3.11.14 because there are two confusing packages: `whisper` (an unrelated library) and `openai-whisper` (the actual AI model).
**Root Cause**: Installing just `pip install whisper` installs the wrong package.
**Solution**:
1.  **Uninstall the bad package**:
    ```powershell
    pip uninstall whisper
    pip uninstall openai-whisper
    ```
2.  **Install the correct package**:
    ```powershell
    pip install openai-whisper
    ```
3.  **Code Check**: Ensure your code imports it correctly (though we switched to Google Speech Recognition for speed, this applies if you go back to Whisper).

### 🔴 `AttributeError: 'start_new_thread' (in PyAudio)`
**Context**: Python 3.11 deprecated some threading methods used by old `PyAudio` versions.
**Solution**:
1.  Install the pre-compiled binary for Windows using `pipwin` (if available) or update to the latest wheel:
    ```powershell
    pip install pipwin
    pipwin install pyaudio
    ```
    *Alternative*: `pip install pyaudio --upgrade`

---

## 2. 🖥️ GUI & PyQt6 Errors

### 🔴 `ModuleNotFoundError: No module named 'PyQt6'`
**Context**: The application fails to launch because the GUI framework is missing.
**Solution**:
```powershell
pip install PyQt6
```

### 🔴 `AttributeError: 'QPushButton' object has no attribute 'setHeight'`
**Context**: You tried to set the height of a button, but PyQt6 does not have a `setHeight` method.
**Root Cause**: `setHeight` is not a valid Qt method.
**Solution**: Use **`setFixedHeight(int)`** instead.
```python
# WRONG
self.btn.setHeight(50)

# CORRECT
self.btn.setFixedHeight(50)
```

### 🔴 `qt.qpa.plugin: Could not find the Qt platform plugin "windows"`
**Context**: Running the app, it crashes immediately.
**Root Cause**: Corrupted PyQt6 installation or missing DLLs.
**Solution**: Reinstall the library cleanly.
```powershell
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip
pip install PyQt6
```

---

## 3. 🔊 Audio & Connection Errors

### 🔴 `[WinError 10048] Only one usage of each socket address is normally permitted`
**Context**: You see this when starting `main.py` or the server.
**Root Cause**: The port (usually 5000 or 8000) is already being used by a previous instance of the app that didn't close properly.
**Solution**:
1.  Close ALL **Terminals** and **VS Code** windows.
2.  Open Task Manager (`Ctrl+Shift+Esc`).
3.  Find `python.exe` processes and end them.
4.  Restart the app.

### 🔴 `ConnectionRefusedError` (Ollama)
**Context**: The Brain cannot "think".
**Solution**: Ensure **Ollama** is running in the background. Open a separate terminal and run `ollama serve` or check your system tray.

---

## 4. 📦 "Video" Package Error

### 🔴 `ERROR: Could not find a version that satisfies the requirement video`
**Context**: Installing `requirements.txt` fails.
**Root Cause**: The `video` package does not exist or was a typo in the requirements file.
**Solution**: 
1. Open `requirements.txt`.
2. Delete the line that says `video`.
3. Save and run `pip install -r requirements.txt` again.

---
**Maintained by PushpakO2**
