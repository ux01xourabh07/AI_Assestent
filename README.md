# Shipra AI Voice Assistant 🤖

Shipra is a conversational AI Voice Assistant built with Python, designed to be a friendly, human-like companion. It understands and speaks in **Hinglish** (a mix of Hindi and English), making it perfect for Indian users. It uses Google's **Gemini AI** for intelligence and **Edge TTS** for natural-sounding speech.

## 🌟 Features

- **Human-like Persona**: Shipra behaves like a friend, not a robot. She speaks casually, uses filler words ("Accha", "Haan"), and respects cultural greetings ("Jay Shree Ram", "Namaste").
- **Hinglish Support**: Fully capable of understanding and replying in a mix of Hindi and English.
- **Natural Voice**: Uses `hi-IN-SwaraNeural` voice for realistic Indian pronunciation.
- **Dark Mode UI**: A modern, sleek dark-themed interface built with `CustomTkinter`.
- **Hold-to-Speak**: Simple "Walkie-Talkie" style interaction to avoid accidental activations.
- **Smart Error Handling**: Displays specific error messages on screen for easy debugging.

## 🛠️ Prerequisites

- **Python 3.8+** installed on your system.
- A **Google Gemini API Key** (Get it from [Google AI Studio](https://aistudio.google.com/)).

## 📦 Installation

1.  **Clone the Repository** (or download the files):
    ```bash
    git clone <repository-url>
    cd Shipra-AI
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: You may need to install `PyAudio` separately if pip fails. On Windows, `pip install pipwin && pipwin install pyaudio` often works.*

## ⚙️ Configuration

1.  Create a file named `.env` in the project root directory.
2.  Add your Gemini API Key to it:
    ```env
    GEMINI_API_KEY=your_actual_api_key_here
    ```

## 🚀 How to Run

1.  Run the main application:
    ```bash
    python main.py
    ```
2.  The application window will open.
3.  **Click and Hold** the big green button to speak.
4.  **Release** the button to send your voice command.
5.  Shipra will think and reply with both text and voice.

## 📁 Project Structure

- `main.py`: The core application file containing UI, Voice Logic, and AI integration.
- `requirements.txt`: List of required Python libraries.
- `.env`: Configuration file for keeping your API Key safe (do not commit this file!).
- `list_voices.py`: A utility script to check available TTS voices on your system.

## 🔧 Troubleshooting

- **Microphone Error**: Ensure your microphone is connected and allowed in Windows Privacy settings.
- **Audio Init Error**: If audio fails, try installing `ffmpeg` and adding it to your system PATH.
- **Gemini API Error**: Check your `.env` file and ensure the API Key is valid and has active quota.
- **Window not showing**: Ensure `customtkinter` is installed correctly.

## � Git Workflow

Useful commands for managing the project:

- **Update Project (Pull)**: Get the latest changes from the server/repo.
  ```bash
  git pull origin main
  ```

- **Check Changes**: See what files you have modified.
  ```bash
  git status
  ```

- **Save Changes (Commit)**:
  ```bash
  git add .
  git commit -m "Updated features"
  ```

- **Upload Changes (Push)**:
  ```bash
  git push origin main
  ```

## �🛡️ License

This project is created by **PushpakO2**. Feel free to use and modify!