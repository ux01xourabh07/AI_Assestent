# Shipra AI Assistant - Voice CLI Edition 🤖

**Proprietary AI System by Pushpak O 2**

> **Identity**: Female Persona ("Shipra") | **Core**: Google Gemini 2.5 | **Interface**: Voice-First Console

---

## 📖 Overview

**Shipra AI** has been evolved into a streamlined, low-latency **Command Line Voice Assistant**. Removing the overhead of a GUI, it provides a pure "Jarvis-like" experience where interaction is entirely spoken.

It is engineered to understand and speak **Roman Hinglish**, bridging the gap between English and Hindi communication for the Indian context.

### Key Capabilities
*   **🧠 Intelligent Brain**: Powered by **Google Gemini 2.5 Flash** for rapid, context-aware reasoning.
*   **🎤 Voice-First**: Continuous listening loop using **Google Speech Recognition**.
*   **🗣️ Human-Like Speech**: Uses **Microsoft Edge Statistics (Edge-TTS)** for high-quality neural voices options.
*   **🎭 Voice Conversion (RVC)**: Generating custom character voices (Optional).
*   **📚 Long-Term Memory**: Uses **MongoDB** to index and retrieve knowledge from your local files (`data/` folder).
*   **📹 Video Intelligence**: Can download and analyze YouTube video audio using Gemini's multimodal capabilities.

---

## ⚙️ System Architecture

The system is modularized into three core components:

### 1. The Brain (`brain.py`)
*   **Model**: Gemini 2.5 Flash (`gemini-2.5-flash`).
*   **Memory**: Migrated from ChromaDB to **MongoDB for fast keyword retrieval**.
*   **Function**: Orchestrates the conversation, manages context, and ensures the persona is maintained.

### 2. The Ear (`audio.py` - Listen)
*   **Library**: `SpeechRecognition` (Google Web Speech API).
*   **Features**:
    *   Automatic ambient noise adjustment.
    *   **Manual Mic Selection**: You can specify exactly which microphone to use via `config.py`.

### 3. The Voice (`audio.py` - Speak)
*   **Standard TTS**: `edge-tts` (Free, high-quality neural voices).
*   **RVC Post-Processing**:
    *   If a `.pth` model is found in the `models/` directory, the system attempts to convert the TTS voice into that character's voice using **Retrieval-based Voice Conversion**.
    *   *Note: Requires Visual C++ Build Tools for installation.*

---

## 🚀 Setup & Installation

### Prerequisites
*   **Python 3.10+**
*   **Google API Key** (for Gemini)
*   **Visual C++ Build Tools** (Only if you want RVC support)

### Installation
1.  **Clone/Download** the repository.
2.  **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```
    *(Note: Use a virtual environment `env`)*

### Configuration (`config.py`)
Open `config.py` to customize your experience:
```python
class Config:
    MODEL_NAME = "gemini-2.5-flash"  # The AI Brain
    MIC_INDEX = None                 # Set to an ID (e.g., 1) to use a specific mic
    GOOGLE_API_KEY = "..."           # Your Gemini API Key
```

---

## 🎙️ Usage Guide

### 1. Start the Assistant
Simply run the main script. There is no GUI window; everything happens in the console.

```powershell
python main.py
```

### 2. Interaction
*   **Greeting**: Shipra will introduce herself.
*   **Listening**: When you see `Listening...`, speak clearly into your mic.
*   **Response**: Shipra will print her response and speak it out loud.
*   **Exit**: Say "Exit", "Bye", or "Stop" to close the program.

### 3. Microphone Selection
If Shipra isn't hearing you, you might be using the wrong mic.
1.  Run `python list_mics.py` to see your devices.
2.  Update `MIC_INDEX` in `config.py`.

---

## 📂 Project Structure

*   `main.py`: The entry point. Runs the infinite voice loop.
*   `brain.py`: The cognitive core (LLM & Memory).
*   `audio.py`: Handles Microphone input and Speaker output.
*   `config.py`: Global settings.
*   `memory.py`: MongoDB interface for retrieving knowledge.
*   `data/`: Place your `.md` or `.txt` text files here for Shipra to learn.
*   `models/`: Place RVC `.pth` voice models here.

---

**Developed by Pushpak O 2**