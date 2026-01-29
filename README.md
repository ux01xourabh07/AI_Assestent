# Shipra AI Assistant 🤖

**Proprietary AI System by PushpakO2**

Shipra is a highly advanced, local-first AI assistant designed for speed, privacy, and Indian context efficiency. It runs locally using **Ollama (Llama 3.2)** and **ChromaDB**, with a modern **PyQt6** interface.

## 🚀 Key Features

*   **Intelligence**: Powered by **Llama 3.2 (1B)** via Ollama. Fast, smart, and efficient.
*   **Knowledge Base (RAG)**: Trained on **PushpakO2** internal data.
*   **Voice**:
    *   **Input**: Google Speech Recognition (Fast & Accurate) with ambient noise adjustment.
    *   **Output**: **Edge TTS (Neural)** using `en-IN-PrabhatNeural`.
        *   **Polyglot Capability**: Speaks English in an **Indian Accent** and Hindi in a **native Hindi Accent**.
        *   **Tuning**: Pitch `-5Hz`, Speed `+10%` for a natural, deep male voice.
*   **GUI**:
    *   **Framework**: **PyQt6** (Modern, Thread-Safe).
    *   **Visualizer**: Real-time smooth audio wave animation.
    *   **Status Indicators**: Clear "Listening", "Thinking", "Speaking" states.
*   **Identity**: Professional, Ethical, Male Persona ("James" style), fluent in **Roman Hinglish**.

## 🛠️ Prerequisites

1.  **Ollama**: Must be installed and running.
    *   Model: `ollama pull llama3.2:1b`
    *   Embeddings: `ollama pull nomic-embed-text`
2.  **Python 3.10+**

## 📦 Installation

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Setup Knowledge Base**:
    *   Keep your documents (PDF, MD, JSON, TXT) in the `data/` folder.
    *   Shipra learns them automatically on startup.

## 🏃‍♂️ How to Run

1.  **Start the Assistant**:
    ```bash
    python main.py
    ```
2.  **Interact**:
    *   **Voice**: System listens automatically. Click **MIC ON** to mute.
    *   **Text**: Type in the box and hit ENTER.
    *   **Visualizer**: Watch the ring pulse when Shipra speaks!

## 🧠 Brain Architecture

*   **`main.py`**: Entry point. Launches PyQt6 Application.
*   **`gui.py`**: The UI Layer. Handles Window, Visualizer, and Worker Threads (Signals/Slots).
*   **`brain.py`**: The "Mind". Handles Logic, RAG (Memory), and Persona (LangChain).
*   **`audio.py`**: The "Ears & Mouth". Handles Speech-to-Text and Text-to-Speech.
*   **`systems.py`**: Singleton manager for resource efficiency.

---
**Created by PushpakO2** 🇮🇳