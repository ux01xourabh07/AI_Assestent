# Shipra AI - Distributed Architecture Approach 🚀

**Proprietary Design by PushpakO2**

This document outlines the architectural approach for running Shipra AI in a **Distributed Environment**. In this setup, the heavy AI processing (LLM/Brain) is offloaded to a secondary machine ("Server"), while the primary machine ("Client") handles the User Interface and Audio I/O.

---

## 1. High-Level Architecture

The system is divided into two distinct nodes connected via **Local LAN (Wi-Fi/Ethernet)**.

### 🖥️ Node A: The Client (User's Laptop)
*   **Role**: Frontend & Interaction Layer.
*   **Responsibility**: Lightweight, fast, energy-efficient.
*   **Components**:
    *   **GUI**: built with **PyQt6** (Detailed below).
    *   **Input**: **SpeechRecognition** (Local STT) to capture voice commands.
    *   **Output**: **Edge-TTS** (Local Neural Audio) for speech synthesis.
    *   **Network**: Sends text prompts via HTTP to Node B.

### 💻 Node B: The Server (Heavy Lifter)
*   **Role**: Intelligence & Processing Layer.
*   **Responsibility**: Running the LLM and RAG mechanisms.
*   **Components**:
    *   **API Gateway**: **FastAPI** server exposing endpoints.
    *   **LLM Engine**: **Ollama** running Llama 3.2.
    *   **Memory**: **ChromaDB** storing the Knowledge Base (*PushpakO2 Data*).

---

## 2. 🎨 Detailed GUI Architecture (Node A)

The Frontend is built using **PyQt6** for a native, high-performance experience.

### A. Core Components
1.  **Main Window (`QMainWindow`)**:
    *   Acts as the central container.
    *   Manages the specialized Dark Theme (CSS-like QSS styling).
    *   Handles global key events (e.g., Hotkeys for Mic).
2.  **Audio Visualizer (`QWidget` + `QPainter`)**:
    *   **Rendering**: Uses Custom Paint Events (`paintEvent`) instead of static images.
    *   **Animation**: A `QTimer` triggers updates at 60 FPS.
    *   **Reactive**: The "Circle" expands/contracts based on Amplitude (Simulated or Real Audio Data).
    *   **Colors**: Uses Gradients (Blue/Cyan) for a Futuristic Look.
3.  **Control Panel**:
    *   **Sliders**: Real-time adjustment of Pitch and Speed.
    *   **Mic Toggle**: Custom styled `QPushButton` with Red/Green states.

### B. Threading Model (Crucial for Responsiveness)
To ensure the GUI **never freezes**, we use the `QThread` Worker Pattern:

*   **Main Thread (GUI)**: Handles drawing, clicks, and window movement. **NEVER** does blocking work.
*   **`ListenWorker` (Thread 1)**:
    *   Runs an infinite loop listening to the Microphone.
    *   Uses `pyqtSignal` to send recognized text to the Main Thread.
*   **`BrainWorker` (Thread 2)**:
    *   Handles the Network Request (`requests.post`) to Node B.
    *    Waits for the Server response asynchronously.
*   **`SpeakWorker` (Thread 3)**:
    *   Generates Audio chunks.
    *   Feeds `pygame.mixer` or `PyAudio` stream.

### C. State Management
The UI transitions between 3 clearly defined states:
1.  **LISTENING (Green)**: Mic is active, Visualizer pulses gently.
2.  **THINKING (Cyan)**: Input sent to Server, awaiting response. Visualizer spins/loads.
3.  **SPEAKING (Purple)**: Playing audio response. Visualizer reacts efficiently.

---

## 3. 🔌 API Specification & Data Flow

Communication happens via JSON over HTTP (REST).

### Endpoint: `POST /chat`

**Request (Client -> Server):**
```json
{
  "user_id": "user_01",
  "text": "Pushpak O2 kya hai?",
  "audio_config": {
    "preferred_language": "hi-IN"
  }
}
```

**Response (Server -> Client):**
```json
{
  "response_text": "PushpakO2 ek AI company hai...",
  "sentiment": "positive",
  "context_used": ["doc_id_123"],
  "processing_time_ms": 450
}
```

### Error Handling
*   **Timeout**: If Server doesn't reply in 10s, Client says "Server Unreachable".
*   **Offline**: If connection fails, Client switches to a "Local Fallback" mode (if configured) or shows a connection error icon.

---

## 4. Implementation Strategy

### Step 1: Backend Setup (Node B)
Create a `server_node.py` on the second laptop:
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama import OllamaLLM

app = FastAPI()
llm = OllamaLLM(model="llama3.2:1b")

class ChatRequest(BaseModel):
    text: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        response = llm.invoke(req.text)
        return {"response_text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```
Run with: `uvicorn server_node:app --host 0.0.0.0 --port 8000`

### Step 2: Client Connection (Node A)
Configure `config.py` on the main laptop to point to the server:
```python
class Config:
    # Instead of local, we point to the LAN IP of the second laptop
    BRAIN_API_URL = "http://192.168.1.XX:8000/chat"
```

### Step 3: Frontend Client Logic
Modify `brain.py` to use `requests`:
```python
def chat(self, text):
    try:
        res = requests.post(Config.BRAIN_API_URL, json={"text": text}, timeout=10)
        return res.json().get("response_text")
    except:
        return "Server error."
```

---

## 5. Security & Deployment

*   **Firewall**: Ensure Node B allows inbound traffic on Port 8000.
*   **Static IP**: Assign a Static IP to Node B so Node A's config doesn't need constant updating.
*   **Authentication**: Add a simplified API Key header `x-api-key: shipra-secret-123` to prevent unauthorized access on the network.

---
**Architected by PushpakO2**
