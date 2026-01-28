import asyncio
import os
import threading
import io
import pygame
import speech_recognition as sr
import numpy as np
import whisper
import edge_tts
from langdetect import detect

class ShipraAudio:
    def __init__(self):
        # STT Setup
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 400
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        print("STT: Using Google Speech Recognition")
        # self.stt_model = whisper.load_model("tiny") # Disabled for SR
        print("Audio System Ready.")

        # Audio Output Setup
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Audio Init Warning: {e}")
            
        self.volume = 1.0
        self.lock = threading.Lock()

    def set_volume(self, volume):
        """Sets the volume for the audio output."""
        try:
            self.volume = float(volume)
            # Apply immediately if music is playing
            if pygame.mixer.get_init():
                pygame.mixer.music.set_volume(self.volume)
        except Exception as e:
            print(f"Error setting volume: {e}")

    def normalize_text(self, text):
        replacements = {
            "AI": "Artificial Intelligence",
            "API": "A P I",
            "Shipra": "Ship-raa",
            "OK": "Okay",
            "ok": "okay"
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    def detect_language(self, text):
        try:
            lang = detect(text)
            return "hi" if lang == "hi" else "en"
        except:
            return "en"

    def listen(self):
        """
        Listens to microphone, converts to numpy, and uses Whisper.
        Bypasses FFmpeg file read issues.
        """
        with sr.Microphone(sample_rate=16000) as source:
            # print("Listening (Whisper)...") # Verbose off
            try:
                # self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                
                # Capture Audio
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                
                # Transcribe using Google Web Speech API (SR)
                # Much faster and lighter than running local Whisper
                try:
                    text = self.recognizer.recognize_google(audio)
                    return text
                except sr.UnknownValueError:
                    return None
            except Exception as e:
                # print(f"Listening error: {e}")
                return None

    async def _generate_edge_tts(self, text, lang):
        """Generate TTS to memory buffer."""
        # SwaraNeural handles both English and Roman-Hindi (Hinglish) beautifully.
        voice = "hi-IN-MadhurNeural"
        
        # Natural conversational speed
        communicate = edge_tts.Communicate(text, voice, rate="+0%")
        
        # Stream to bytes
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return audio_data

    def speak(self, text, on_start=None, on_end=None):
        def play_thread():
            with self.lock:
                try:
                    lang = self.detect_language(text)
                    clean_text = self.normalize_text(text)
                    print(f"Shipra ({lang}): {clean_text}")
                    
                    # Generate audio to memory
                    audio_data = asyncio.run(self._generate_edge_tts(clean_text, lang))
                    
                    if on_start: on_start()
                    
                    # Play from memory buffer
                    pygame.mixer.music.load(io.BytesIO(audio_data))
                    pygame.mixer.music.set_volume(self.volume)
                    pygame.mixer.music.play()
                    
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(50)
                        
                except Exception as e:
                    print(f"Audio Error: {e}")
                finally:
                    try:
                        pygame.mixer.music.unload()
                    except: pass
                    if on_end: on_end()

        threading.Thread(target=play_thread, daemon=True).start()
