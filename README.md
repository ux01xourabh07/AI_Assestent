# Gemini Voice Assistant

A modern AI voice assistant powered by Google's Gemini API with speech recognition and text-to-speech capabilities.

## Features

- 🎤 **Voice Input** - Hold-to-speak functionality
- 🤖 **Gemini AI** - Powered by Google's advanced AI
- 🔊 **Voice Output** - Natural text-to-speech responses
- 🎨 **Modern GUI** - Clean dark theme interface
- 🔄 **Real-time** - Live status updates and clock
- 🛡️ **Secure** - API key stored in environment variables

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/SAGE-Rebirth/gemini-voice-assistant.git
cd gemini-voice-assistant
```

### 2. Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install PyAudio (Windows)
If PyAudio installation fails on Windows:
```bash
# Option 1: Use conda
conda install pyaudio

# Option 2: Download wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
# Then install: pip install PyAudio-0.2.11-cp39-cp39-win_amd64.whl
```

### 5. Get Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 6. Configure Environment
1. Open `.env` file in the project directory
2. Replace `your-gemini-api-key-here` with your actual API key:
```
GEMINI_API_KEY=AIzaSyBcN5AkDFqIguEBfivKcy-RYBcMmMjPh3I
```

### 7. Run the Assistant
```bash
python main.py
```

## Usage

1. **Launch** the application
2. **Hold** the green "HOLD TO SPEAK" button
3. **Speak** your question or command
4. **Release** the button to send
5. **Listen** to the AI response

## System Requirements

- **Python 3.7+**
- **Microphone** access
- **Internet connection** (for Gemini API and speech recognition)
- **Audio output** (speakers/headphones)

## Troubleshooting

### Microphone Issues
```bash
# Test microphone access
python -c "import speech_recognition as sr; print('Microphones:', sr.Microphone.list_microphone_names())"
```

### PyAudio Installation Issues
- **Windows**: Use conda or download pre-compiled wheel
- **macOS**: `brew install portaudio` then `pip install pyaudio`
- **Linux**: `sudo apt-get install portaudio19-dev` then `pip install pyaudio`

### API Key Issues
- Ensure API key is correctly set in `.env` file
- Check API key has proper permissions
- Verify internet connection

### Speech Recognition Issues
- Speak clearly and at normal pace
- Ensure microphone permissions are granted
- Check microphone is not muted
- Try in a quiet environment

## Project Structure

```
gemini-voice-assistant/
├── main.py              # Main application
├── requirements.txt     # Python dependencies
├── .env                # API key configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Dependencies

- **customtkinter** - Modern GUI framework
- **speechrecognition** - Speech-to-text conversion
- **pyttsx3** - Text-to-speech synthesis
- **pyaudio** - Audio input/output
- **openai** - API client for Gemini
- **python-dotenv** - Environment variable management
- **pocketsphinx** - Offline speech recognition fallback

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Ensure all dependencies are installed
3. Verify API key configuration
4. Create an issue on GitHub with error details