# Shipra AI - Voice-First CLI Architecture 🚀

**Proprietary Design by Pushpak O2**

This document outlines the architectural approach for Shipra AI - a streamlined **Voice-First Command Line Assistant** designed for Pushpak O2.

---

## 1. High-Level Architecture

The system runs entirely on the **User's Machine**, with cloud connectivity for AI intelligence.

### 💻 The Client (User's Machine)
*   **Role**: Voice-first interface with automatic language detection.
*   **Responsibility**: Audio I/O, Language Processing, API Communication.
*   **Components**:
    *   **Interface**: Command Line (no GUI overhead).
    *   **Input**: **Google Speech Recognition** (Cloud STT).
    *   **Output**: **Edge-TTS** with Indian voice (en-IN-NeerjaNeural).
    *   **Brain**: **Google Gemini 2.5 Flash** API for intelligence.
    *   **Knowledge Base**: Local markdown files for company and vehicle information.

---

## 2. 🧠 Brain Architecture (`brain.py`)

### A. Core Components
1.  **Language Detection System**:
    *   Automatic detection of English vs Hinglish.
    *   Keyword-based analysis (20+ Hindi keywords).
    *   Devanagari script detection.
    *   "english" keyword override.

2.  **Knowledge Base**:
    *   **Company Data**: `Pushpak_Company.md` (leadership, location, mission).
    *   **Vehicle Data**: `Pushpak_Vehicle.md` (capacity, features, compliance).

3.  **Response System**:
    *   Varied responses (3 variations per response type).
    *   Counter-based rotation to avoid repetition.
    *   Bilingual responses (English + Roman Hinglish).

### B. Language Detection Algorithm
```
Input: User text
↓
Check for "english" keyword → English mode
↓
Detect Devanagari characters → Hinglish mode
↓
Count Hindi keywords (kaun, kya, kaise, hai, etc.)
↓
If >20% Hindi keywords → Hinglish mode
↓
Default → English mode
```

---

## 3. 🎙️ Audio Architecture (`audio.py`)

### A. Speech Recognition
*   **Engine**: Google Web Speech API.
*   **Features**:
    *   Ambient noise adjustment.
    *   Configurable microphone selection.
    *   Robust error handling.
    *   Timeout management.

### B. Text-to-Speech
*   **Engine**: Microsoft Edge TTS.
*   **Voice**: `en-IN-NeerjaNeural` (Indian English female).
*   **Settings**:
    *   Pitch: `-10Hz` (natural tone).
    *   Rate: `+25%` (responsive speed).
*   **Language Support**: 
    *   English pronunciation.
    *   Roman Hinglish pronunciation.

---

## 4. 🔄 Data Flow

### Conversation Flow
```
1. LISTEN
   User speaks → Google STT → Text
   ↓
2. DETECT LANGUAGE
   Analyze keywords → English/Hinglish mode
   ↓
3. PROCESS QUERY
   Match query type → Company/Vehicle/General
   ↓
4. RETRIEVE KNOWLEDGE
   Load from markdown files → Extract relevant info
   ↓
5. GENERATE RESPONSE
   Select varied response → Apply language mode
   ↓
6. SPEAK
   Edge TTS → Audio output
```

---

## 5. 📊 Response Variety System

### Mechanism
- Each response type has 3 pre-written variations.
- Counter tracks which variation was last used.
- Rotates through variations using modulo operation.
- Prevents repetitive answers in consecutive queries.

### Example
```python
responses = [
    "Response variation 1",
    "Response variation 2",
    "Response variation 3"
]
response = responses[counter % 3]
counter += 1
```

---

## 6. 🔒 Security & Configuration

*   **API Key**: Stored in `config.py` (excluded from git via `.gitignore`).
*   **Privacy**: All knowledge base files stored locally.
*   **No Data Collection**: Voice processing happens via standard APIs.

---

## 7. 📝 Knowledge Base Structure

### Company Information (`Pushpak_Company.md`)
- Company name and aliases
- Leadership team (President, Technology Lead)
- Location and headquarters
- Mission and focus areas

### Vehicle Specifications (`Pushpak_Vehicle.md`)
- Capacity (persons and load)
- Technical features (AI, hydrogen, autonomous)
- Compliance standards (DGCA)
- System type (UAS)

---

## 8. 🔧 Technical Stack

| Component | Technology |
|-----------|------------|
| AI Brain | Google Gemini 2.5 Flash |
| STT | Google Speech Recognition |
| TTS | Microsoft Edge TTS |
| Language | Python 3.10+ |
| Interface | Command Line |
| Knowledge | Markdown files |
| Version Control | Git/GitHub |

---

**Architected by Pushpak O2**  
**AI Assistant: Shipra**
