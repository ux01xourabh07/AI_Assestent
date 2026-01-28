# Systems Singleton Module
# This ensures we only load heavy models (LLM, Whisper) ONCE.

from brain import ShipraBrain
from audio import ShipraAudio

class Systems:
    _brain = None
    _audio = None
    
    @classmethod
    def get_brain(cls):
        if cls._brain is None:
            print("Initializing Brain (Singleton)...")
            cls._brain = ShipraBrain()
        return cls._brain
        
    @classmethod
    def get_audio(cls):
        if cls._audio is None:
            print("Initializing Audio System (Singleton)...")
            cls._audio = ShipraAudio()
        return cls._audio
