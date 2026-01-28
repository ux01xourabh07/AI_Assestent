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
        
        print("Loading Whisper Model (Tiny)...")
        self.stt_model = whisper.load_model("tiny")
        print("Whisper Loaded (Tiny).")

        # Audio Output Setup
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Audio Init Warning: {e}")
            
        self.volume = 1.0
        self.lock = threading.Lock()

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
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                # Capture Audio
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=8)
                
                # Convert to Numpy for Whisper (Bypass FFmpeg)
                # Get raw data: 16-bit PCM, 16kHz (set in Microphone)
                raw_data = audio.get_raw_data(convert_rate=16000, convert_width=2)
                
                # Convert byte buffer to numpy float32 array
                np_audio = np.frombuffer(raw_data, dtype=np.int16).astype(np.float32) / 32768.0
                
                # Transcribe
                result = self.stt_model.transcribe(np_audio, fp16=False) # fp16=False for compatibility
                text = result["text"].strip()
                
                if not text: return None
                return text

            except (sr.WaitTimeoutError, sr.UnknownValueError):
                return None
            except Exception as e:
                print(f"STT Error: {e}")
                return None

    async def _generate_edge_tts(self, text, lang):
        """Generate TTS to memory buffer."""
        voice = "hi-IN-SwaraNeural" if lang == "hi" else "en-IN-NeerjaNeural"
        
        # Speed up slightly for conversational flow
        communicate = edge_tts.Communicate(text, voice, rate="+5%")
        
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
