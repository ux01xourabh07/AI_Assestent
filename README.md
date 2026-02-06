# Shipra AI Assistant - Voice CLI Edition 🤖

**Proprietary AI System by Pushpak O2**

> **Identity**: Female Persona ("Shipra") | **Core**: Google Gemini 2.5 Flash | **Interface**: Voice-First Console

---

## 📖 Overview

**Shipra AI** is a streamlined, low-latency **Command Line Voice Assistant** for Pushpak O2. It provides a pure "Jarvis-like" experience where interaction is entirely spoken.

Engineered to understand and speak both **English** and **Roman Hinglish**, automatically detecting the language based on user input.

### Key Capabilities
*   **🧠 Intelligent Brain**: Powered by **Google Gemini 2.5 Flash** for rapid, context-aware reasoning.
*   **🎤 Voice-First**: Continuous listening loop using **Google Speech Recognition**.
*   **🗣️ Human-Like Speech**: Uses **Microsoft Edge TTS (en-IN-NeerjaNeural)** with Indian accent, optimized pitch (-10Hz) and speed (+25%).
*   **🌐 Bilingual Support**: Automatic language detection - responds in English or Roman Hinglish based on user input.
*   **📚 Company Knowledge**: Integrated knowledge base about Pushpak O2 company and vehicle specifications.
*   **🎯 Smart Responses**: Varied response system to avoid repetition.

---

## ⚙️ System Architecture

The system is modularized into core components:

### 1. The Brain (`brain.py`)
*   **Model**: Gemini 2.5 Flash (`gemini-2.5-flash`).
*   **Language Detection**: Automatic detection of English/Hinglish based on keywords and sentence structure.
*   **Knowledge Base**: Company information (Pushpak_Company.md) and Vehicle specifications (Pushpak_Vehicle.md).
*   **Response Variety**: Counter-based system to provide varied responses.

### 2. The Ear (`audio.py` - Listen)
*   **Library**: `SpeechRecognition` (Google Web Speech API).
*   **Features**:
    *   Automatic ambient noise adjustment.
    *   **Manual Mic Selection**: Specify microphone via `config.py`.
    *   Robust error handling for speech recognition.

### 3. The Voice (`audio.py` - Speak)
*   **TTS Engine**: `edge-tts` with Indian voice (en-IN-NeerjaNeural).
*   **Voice Settings**: 
    *   Pitch: -10Hz (natural female voice)
    *   Rate: +25% (faster, more responsive)
*   **Language Support**: Pronounces both English and Roman Hinglish correctly.

---

## 🚀 Setup & Installation

### Prerequisites
*   **Python 3.10+**
*   **Google API Key** (for Gemini)

### Installation
1.  **Clone the repository**:
    ```powershell
    git clone https://github.com/SAGE-Rebirth/gemini-voice-assistant.git
    cd gemini-voice-assistant
    ```

2.  **Install Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```

3.  **Configure API Key**:
    Open `config.py` and add your Google API key:
    ```python
    class Config:
        MODEL_NAME = "gemini-2.5-flash"
        MIC_INDEX = None  # Set to specific mic ID if needed
        GOOGLE_API_KEY = "your-api-key-here"
    ```

---

## 🎙️ Usage Guide

### 1. Start the Assistant
```powershell
python main.py
```

### 2. Language Modes
Shipra automatically detects and responds in the appropriate language:

**English Mode** (triggered by):
- Pure English sentences: "What is the vehicle capacity?"
- Keyword "english": "Tell me about the company in english"

**Hinglish Mode** (triggered by):
- Hindi keywords: "President kaun hai?"
- Mixed sentences: "Vehicle ki capacity kya hai?"
- Devanagari script (auto-converted to Roman Hinglish)

### 3. Interaction Examples

**Company Information:**
- "Who is the president?" → English response
- "Founder kaun hai?" → Hinglish response
- "Tell me about Pushpak O2" → English response
- "Company ke baare mein batao" → Hinglish response

**Vehicle Information:**
- "What is the load capacity?" → English response
- "Vehicle ki capacity kya hai?" → Hinglish response
- "Tell me the features" → English response
- "Features kya hain?" → Hinglish response

**Weather Information:**
- "What's the weather?" → English response with current weather
- "Mausam kaisa hai?" → Hinglish response with current weather
- "Tomorrow's forecast" → English response with forecast
- "Kal ka mausam kya hoga?" → Hinglish response with forecast

### 4. Exit Commands

**Company Information:**
- "Who is the president?" → English response
- "Founder kaun hai?" → Hinglish response
- "Tell me about Pushpak O2" → English response
- "Company ke baare mein batao" → Hinglish response

**Vehicle Information:**
- "What is the load capacity?" → English response
- "Vehicle ki capacity kya hai?" → Hinglish response
- "Tell me the features" → English response
- "Features kya hain?" → Hinglish response

### 4. Exit Commands
Say: "Exit", "Bye", "Stop", "Alvida", or "Tata"

### 5. Microphone Setup
If Shipra isn't hearing you:
1.  Run `python list_mics.py` to see available devices.
2.  Update `MIC_INDEX` in `config.py` with the correct device number.

---

## 📂 Project Structure

```
Assistent/
├── main.py              # Entry point - voice interaction loop
├── brain.py             # AI logic, language detection, responses
├── audio.py             # Speech recognition and TTS
├── config.py            # Configuration settings
├── data/
│   ├── Pushpak_Company.md   # Company information
│   └── Pushpak_Vehicle.md   # Vehicle specifications
├── requirements.txt     # Python dependencies
└── .gitignore          # Git ignore rules
```

---

## 🔧 Technical Details

### Language Detection Algorithm
- Checks for "english" keyword → English mode
- Detects Hindi keywords (kaun, kya, kaise, hai, mein, etc.)
- Analyzes Devanagari characters
- Calculates Hindi keyword ratio (>20% = Hinglish mode)
- Defaults to English for pure English input

### TTS Configuration
- Voice: `en-IN-NeerjaNeural` (Indian English female)
- Pitch: `-10Hz` (natural tone)
- Rate: `+25%` (responsive speed)
- Output: Roman Hinglish for proper pronunciation

### Response Variety System
- Each response type has 3 variations
- Counter tracks usage to rotate responses
- Prevents repetitive answers

---

## 📝 Knowledge Base

### Company Information (Pushpak_Company.md)
- **Name**: Pushpak O2 (also recognized as "Pushpak auto")
- **Leadership**: 
  - Aditya Shrivastava - President & Co-Founder
  - Aneerudh Kumar - Technology Lead & Co-Founder
- **Location**: Bhopal, Madhya Pradesh
- **Focus**: Indigenous aviation platforms and unmanned aerial systems

### Vehicle Specifications (Pushpak_Vehicle.md)
- **Capacity**: 4 persons OR 500kg load
- **Features**: AI autonomous flight, obstacle detection, hydrogen fuel cell
- **Compliance**: DGCA standards
- **Type**: Advanced unmanned aerial system (UAS)

---

## 🔗 Repository

**GitHub**: [https://github.com/SAGE-Rebirth/gemini-voice-assistant.git](https://github.com/SAGE-Rebirth/gemini-voice-assistant.git)

---

**Developed by Pushpak O2**  
**AI Assistant: Shipra**