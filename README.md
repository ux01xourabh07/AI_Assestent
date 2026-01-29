# Shipra AI Assistant (v2.0) 🤖

**Proprietary AI System by PushpakO2**

> **Identity**: Female Persona ("Neerja" Style) | **Language**: Roman Hinglish | **Core**: Llama 3.2 (Local)

---

## 📖 Table of Contents
1.  [About the Project](#about-the-project)
2.  [System Architecture](#system-architecture)
3.  [Requirements & Prerequisites](#requirements--prerequisites)
4.  [Installation Guide](#installation-guide)
5.  [Usage Guide (The Interface)](#usage-guide-the-interface)
6.  [Voice Tuning & Personalization](#voice-tuning--personalization)
7.  [Under the Hood: How it Works](#under-the-hood-how-it-works)
8.  [Troubleshooting](#troubleshooting)

---

## 1. About the Project

**Shipra AI** is a state-of-the-art, local-first Desktop Assistant built specifically for the Indian context. Unlike generic assistants, Shipra is engineered to understand and speak **Roman Hinglish** fluently, bridging the gap between English and Hindi communication.

It moves away from distinct "Text Mode" and "Voice Mode" into a unified **PyQt6** interface where visual feedback, voice interaction, and text chat coexist seamlessly.

### Key Capabilities
*   **Local Intelligence**: Runs completely offline for logic (using Ollama), providing maximum privacy.
*   **Polyglot Voice**: Uses advanced Neural TTS to speak English with an Indian accent and Hindi with a native Hindi accent, switching contextually within the same sentence.
*   **Real-Time Tuning**: Modify the voice pitch and speed instantly via the GUI.
*   **Memory (RAG)**: Learns from your local documents (`data/` folder) to provide context-aware answers.

---

## 2. System Architecture

The project is modularized for efficiency and ease of maintenance:

### 🧠 The Brain (`brain.py`)
*   **Model**: Llama 3.2 (1 Billion Parameters) via Ollama. 
*   **Reasoning**: It receives user input, retrieves relevant context from the Vector Database (ChromaDB), and generates a concise, Hinglish response.
*   **Persona**: Strictly conditioned to be a helpful, ethical, female assistant.

### 👂 & 🗣️ The Audio System (`audio.py`)
*   **Input (Ears)**: Uses `SpeechRecognition` with Google's API for high-accuracy Speech-to-Text (STT). It features ambient noise adjustment to detect voice even in noisy rooms.
*   **Output (Mouth)**: Uses `edge-tts` (Microsoft Edge Neural Voices) for ultra-realistic speech.
*   **Dynamic Tuning**: Supports real-time adjustment of **Pitch** (Hz) and **Rate** (BPM).

### 👁️ The GUI (`gui.py`)
*   **Framework**: **PyQt6** (Python Qt).
*   **Visualizer**: A custom-painted high-FPS wave visualizer that reacts to the assistant's state.
*   **Threading**: Uses `QThread` workers to ensure the interface never freezes, even when the AI is "thinking" or "listening".

---

## 3. Requirements & Prerequisites

Before you begin, ensure your system meets these specifications:

### Hardware
*   **OS**: Windows 10/11 (Preferred)
*   **RAM**: 8GB Minimum (16GB Recommended)
*   **Microphone**: Functional input device.
*   **Internet**: Required for STT (Google) and TTS (Edge).

### Software
1.  **Python 3.10 or newer**: [Download Here](https://www.python.org/downloads/)
2.  **Ollama**: The local LLM runner. [Download Here](https://ollama.com/)
    *   **Action Required**: Open your terminal and run:
        ```bash
        ollama pull llama3.2:1b
        ollama pull nomic-embed-text
        ```

---

## 4. Installation Guide

Follow these steps to set up Shipra AI from scratch.

### Step 1: Clone or Download
Download the project source code to your local machine (e.g., `D:\Assistant`).

### Step 2: Create Environment (Optional but Recommended)
```powershell
python -m venv env
.\env\Scripts\activate
```

### Step 3: Install Dependencies
We have a curated list of libraries in `requirements.txt`.
```powershell
pip install -r requirements.txt
```
*Key Libraries installed: `PyQt6`, `langchain`, `chromadb`, `speechrecognition`, `edge-tts`, `pygame`.*

---

## 5. Usage Guide (The Interface)

Run the application:
```powershell
python main.py
```

### The Dashboard
*   **Visualizer (Center)**: The glowing blue ring is Shipra's "Heartbeat".
    *   **Calm**: Listening / Idle.
    *   **Chaotic/Fast**: Speaking.
*   **Chat Log**: Displays the conversation history.
*   **Input Box**: Type commands manually if you prefer not to speak.

### Controls
*   **MIC ON/OFF**: Toggle this button to mute the microphone. When red (OFF), Shipra stops listening.
*   **Volume**: Master volume slider for Shipra's voice.
*   **Status Label**: Tells you exactly what is happening (`Listening...`, `Thinking...`, `Speaking...`).

---

## 6. Voice Tuning & Personalization

Shipra v2.0 introduces **Dynamic Voice Control**. You can find these sliders in the control panel:

### 🎚️ Pitch (Hz)
*   **Default**: `0 Hz`
*   **Effect**: Makes the voice deeper (Negative) or higher (Positive).
*   **Recommended**: Keep between `-5` and `+5` for a realistic female voice.

### ⏩ Speed (%)
*   **Default**: `+10 %`
*   **Effect**: Makes the assistant speak faster (Positive) or slower (Negative).
*   **Recommended**: `+10%` to `+20%` makes the conversation feel more snappy and less robotic.

*Changes apply immediately to the NEXT sentence spoken.*

---

## 7. Under the Hood: How it Works

### The Interaction Loop
1.  **Wake**: The `ListenWorker` thread monitors the mic. When it detects a phrase, it converts Audio -> Text.
2.  **Think**: The text is sent to `BrainWorker`.
    *   It queries `ChromaDB` for any relevant documents in your `data/` folder.
    *   It constructs a prompt with your Identity + Retrieved Context + User Question.
    *   It sends this to **Ollama** (Llama 3.2).
3.  **Speak**: The response text is sent to `SpeakWorker`.
    *   `audio.py` fetches the audio stream from Edge-TTS using the current Pitch/Rate settings.
    *   `pygame` plays the audio stream.
    *   The `Visualizer` animates in sync.

---

## 8. Troubleshooting

For a full list of errors, see [ERROR.md](ERROR.md).

### Quick Fixes
*   **App won't start?** Make sure you activated your environment (`env\Scripts\activate`).
*   **No Voice?** Check your internet. Edge-TTS requires a connection.
*   **Thinking forever?** Ensure Ollama is running (`ollama serve` in a separate terminal).

---

**Developed with ❤️ by PushpakO2**
*Advancng AI for India.*