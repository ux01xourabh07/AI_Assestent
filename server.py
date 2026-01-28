from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import threading
import sys
import os

# Add current directory to path so we can import modules
sys.path.append(os.getcwd())

try:
    from audio import ShipraAudio
except ImportError:
    print("Could not import ShipraAudio. Make sure requirements are installed.")
    sys.exit(1)

app = FastAPI(title="Shipra AI API")

# Initialize Audio Engine
audio_engine = ShipraAudio()

class SpeakRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "Namaste! Shipra API is running."}

@app.get("/speak")
def speak_get(text: str):
    """
    GET endpoint to make Shipra speak.
    Usage: /speak?text=Hello
    """
    if not text:
        raise HTTPException(status_code=400, detail="Text parameter is required")
    
    # We use the existing speak method which runs in a thread
    audio_engine.speak(text)
    
    return {"status": "success", "message": f"Speaking: {text}"}

@app.post("/speak")
def speak_post(request: SpeakRequest):
    """
    POST endpoint to make Shipra speak.
    JSON Body: {"text": "Hello"}
    """
    audio_engine.speak(request.text)
    return {"status": "success", "message": f"Speaking: {request.text}"}

def start_server():
    uvicorn.run(app, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    start_server()
