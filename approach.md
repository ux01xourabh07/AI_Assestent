# Shipra AI - Cloud-Hybrid Architecture Approach 🚀

**Proprietary Design by Pushpak O 2**

This document outlines the architectural approach for running Shipra AI. The system has been streamlined to a **Single Node** architecture, leveraging **Google Gemini (Cloud)** for intelligence while maintaining local control for Audio I/O and UI.

---

## 1. High-Level Architecture

The system runs entirely on the **User's Laptop (Client)**, connected to the internet.

### 🖥️ The Client (User's Laptop)
*   **Role**: All-in-one Interface & logic.
*   **Responsibility**: UI, Audio Processing, API Communication.
*   **Components**:
    *   **GUI**: built with **PyQt6**.
    *   **Input**: **SpeechRecognition** (Local STT).
    *   **Output**: **Edge-TTS** (Local Neural Audio).
    *   **Brain**: Connects to **Google Gemini API** for intelligence.
    *   **Video Intelligence**: `video_processor.py` for YouTube audio transcription & analysis.

---

## 2. 🎨 Detailed GUI Architecture

The Frontend is built using **PyQt6** for a native, high-performance experience.

### A. Core Components
1.  **Main Window (`QMainWindow`)**:
    *   Acts as the central container.
    *   Manages the specialized Dark Theme.
2.  **Audio Visualizer**:
    *   **Reactive**: The "Circle" expands/contracts based on Amplitude.
3.  **Control Panel**:
    *   **Sliders**: Real-time adjustment of Pitch and Speed.

### B. Threading Model
*   **Main Thread**: GUI rendering.
*   **`ListenWorker`**: Background thread for Microphone listening.
*   **`BrainWorker`**: Background thread for API calls to Google Gemini.
*   **`SpeakWorker`**: Background thread for TTS generation and playback.

---

## 3. 🔌 Data Flow

### API: Google Gemini 1.5 Flash
*   **Input**: User Text + Context (from local RAG).
*   **Output**: JSON Execution Plan + Final Response.

### Flow
1.  **Listen**: Capture Audio -> Text.
2.  **Retrieve**: Search local `chroma_db` for context.
3.  **Think**: Send Prompt to Google Gemini API.
4.  **Speak**: Play returned response using Edge-TTS.

---

## 4. Security & Deployment

*   **API Key**: Secured in `.env` file (never hardcoded).
*   **Privacy**: Local RAG ensures documents stay on the machine; only relevant snippets are sent to the cloud for processing.

---
**Architected by Pushpak O 2**
