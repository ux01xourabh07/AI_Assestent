from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import threading
from systems import Systems
from config import Config

# Initialize App
app = FastAPI(title="Shipra AI API", description="API for Shipra Voice Assistant")

# Initialize Cores via Singleton
Config.ensure_directories()
brain = Systems.get_brain()
audio = Systems.get_audio()

class SpeakRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Shipra AI Server is Running", "status": "online"}

@app.get("/speak")
def speak_get(text: str):
    """
    GET endpoint to make Shipra speak.
    Example: /speak?text=Hello
    """
    try:
        # Run in thread to not block API
        audio.speak(text)
        return {"status": "success", "message": f"Speaking: {text}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/speak")
def speak_post(request: SpeakRequest):
    """
    POST endpoint to make Shipra speak.
    Body: {"text": "Hello"}
    """
    try:
        audio.speak(request.text)
        return {"status": "success", "message": f"Speaking: {request.text}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat")
def chat_get(text: str):
    """
    GET endpoint to chat with Shipra (Text only).
    """
    try:
        response = brain.chat(text)
        return {"status": "success", "user": text, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
