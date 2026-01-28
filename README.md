# Shipra AI Assistant 🤖

**Proprietary AI System by PushpakO2**

Shipra (now also supporting a **Male Persona**) is a highly advanced, local-first AI assistant designed for speed, privacy, and Indian context efficiency. It runs completely locally (except for Speech Recognition) using **Ollama (Llama 3.2)** and **ChromaDB**.

## 🚀 Key Features

*   **Intelligence**: Powered by **Llama 3.2 (1B)** via Ollama. Fast, smart, and efficient.
*   **Knowledge Base (RAG)**: Trained on **PushpakO2** internal data. Ask "Pushpak O2 kya hai?" to see it in action.
*   **Voice**:
    *   **Input**: Google Speech Recognition (Fast & Accurate).
    *   **Output**: Edge TTS (`hi-IN-MadhurNeural` for Male, `hi-IN-SwaraNeural` for Female) for perfect **Hinglish** pronunciation.
*   **Persona**:
    *   **Gender**: Male (current active) / Female (switchable).
    *   **Tone**: Professional, Ethical, Smart, and fluent in **Roman Hinglish**.
*   **GUI**: Modern Dark Theme UI with Real-time Audio Visualizer and Mic Toggle.

## 🛠️ Prerequisites

1.  **Ollama**: Must be installed and running.
    *   Model: `ollama pull llama3.2:1b`
    *   Embeddings: `ollama pull nomic-embed-text`
2.  **Python 3.10+**

## 📦 Installation

1.  **Install Python Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Setup Knowledge Base**:
    *   Keep your documents (PDF, MD, JSON, TXT) in the `data/` folder.
    *   Shipra will learn them automatically or via `/train` command.

## 🏃‍♂️ How to Run

1.  **Start the Assistant**:
    ```bash
    python main.py
    ```
2.  **Interact**:
    *   **Voice**: System listens automatically. Click "MIC ON/OFF" to toggle privacy.
    *   **Text**: Type in the box and hit ENTER.

## 🧠 Brain Architecture

*   **`main.py`**: Unified entry point (GUI + API).
*   **`brain.py`**: The "Mind". Handles Logic, RAG (Memory), and Persona (LangChain).
*   **`audio.py`**: The "Ears & Mouth". Handles Speech-to-Text (Google) and Text-to-Speech (Edge).
*   **`systems.py`**: Singleton manager to ensure efficient resource usage.

## 🔧 Troubleshooting

*   **"Port 5000 Error"**: Close any old running python terminals.
*   **"Ollama Error"**: Ensure Ollama app is running in the background.

---
**Created by PushpakO2** 🇮🇳