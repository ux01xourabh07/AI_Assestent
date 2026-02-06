
import speech_recognition as sr
import pygame
import edge_tts
import asyncio
import os
import time
import nest_asyncio
import glob
from config import Config

# Try importing RVC
# RVC Removed as per user request

# Check if we are running in an event loop (e.g., Jupyter or some GUIs)
try:
    asyncio.get_running_loop()
    nest_asyncio.apply()
except RuntimeError:
    pass

class ShipraAudio:
    def __init__(self):
        print("[Audio] Initializing Audio System...")
        
        # Initialize Speech Recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.pause_threshold = 0.8
        
        print(f"[Audio] Selected Mic Index: {Config.MIC_INDEX if Config.MIC_INDEX is not None else 'Default'}")
        self.microphone = sr.Microphone(device_index=Config.MIC_INDEX)
        
        # Initialize Pygame Mixer for playback
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"[Audio] Pygame Init Error: {e}")

        # Voice Settings - User Custom (20Hz, ~170wpm)
        self.voice = "en-IN-NeerjaNeural" 
        self.rate = "+22%"  # Approx 170 wpm
        self.volume = "+10%"
        self.pitch = "+18Hz"  # User specified

    def set_voice_params(self, pitch_hz, rate_percent):
        self.pitch = f"{pitch_hz:+}Hz"
        self.rate = f"{rate_percent:+}%"

    def set_volume(self, volume_float):
        # edge-tts volume is usually percentage based string like "+10%"
        # Mapping 0.0-1.0 to percentage
        vol_int = int((volume_float - 0.5) * 100) # Range -50% to +50% roughly
        self.volume = f"{vol_int:+}%"

    def normalize_text(self, text):
        clean = text.replace("*", "").replace("#", "")
        return clean

    def listen(self):
        """Captures audio from the microphone and converts to text."""
        with self.microphone as source:
            print("\nListening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                return None

        try:
            print("Recognizing...")
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("[Audio] Network Error during Recognition.")
            return None
        except Exception as e:
            print(f"[Audio] Listen Error: {e}")
            return None

    def speak(self, text, on_start=None, on_end=None):
        """Generates and plays TTS audio using EdgeTTS."""
        if not text: return
        
        clean_text = self.normalize_text(text)
        print(f"\n[Shipra] RESPONSE: {clean_text}")
        
        if on_start: on_start()
        
        tts_file = "response_tts.mp3"
        
        # Generate and Play TTS
        asyncio.run(self._generate_edge_tts(clean_text, tts_file))
        self._play_audio(tts_file)
        
        if on_end: on_end()

    async def _generate_edge_tts(self, text, filename):
        # Use Indian accent with decreased pitch and increased speed for human-like voice
        communicate = edge_tts.Communicate(
            text, 
            self.voice, 
            rate=self.rate,  # +25% faster
            volume=self.volume, 
            pitch=self.pitch  # -15Hz for natural tone
        )
        await communicate.save(filename)

    def _play_audio(self, filename):
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            pygame.mixer.music.unload()
        except Exception as e:
            print(f"[Audio] Playback Error: {e}")
