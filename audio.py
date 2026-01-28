import asyncio
import os
import threading
import pygame
import speech_recognition as sr
from langdetect import detect
import edge_tts

class ShipraAudio:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 400  # Better voice detection
        self.recognizer.dynamic_energy_threshold = True  # Auto-adjust
        self.recognizer.pause_threshold = 0.8  # Shorter pause detection
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)  # Stable settings
        self.volume = 0.7  # Default volume
        self.lock = threading.Lock()
        print("Audio initialized for continuous operation")

    def normalize_text(self, text):
        """Fixes pronunciation and abbreviations."""
        replacements = {
            "AI": "Artificial Intelligence",
            "API": "A P I",
            "Shipra": "Ship-raa",
            "Pushpak O2": "Pushpak O Two",
            "Pushpaak O2": "Pushpak O Two",
            "Pushpak O 2": "Pushpak O Two",
            "Pushpaak O 2": "Pushpak O Two",
            "Pushpak": "Pushpak",
            "Pushpaak": "Pushpak",
            "OK": "Okay",
            "ok": "okay"
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    def detect_language(self, text):
        """Detects if text is Hindi (hi) or English (en)."""
        try:
            lang = detect(text)
            return "hi" if lang == "hi" else "en"
        except:
            return "en"

    def listen(self):
        """Continuous listening with proper loop support."""
        with sr.Microphone() as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio)
                return text.strip() if text else None
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                return None
            except Exception:
                return None

    async def _generate_edge_tts(self, text, lang):
        """Generate TTS to memory buffer."""
        voice = "hi-IN-SwaraNeural" if lang == "hi" else "en-IN-NeerjaNeural"
        communicate = edge_tts.Communicate(text, voice, rate="+10%")
        
        # Generate to bytes buffer instead of file
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return audio_data

    def set_volume(self, volume):
        """Set audio volume (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)

    def speak(self, text, on_start=None, on_end=None):
        def play_thread():
            with self.lock:
                try:
                    lang = self.detect_language(text)
                    clean_text = self.normalize_text(text)
                    
                    # Generate audio to memory
                    audio_data = asyncio.run(self._generate_edge_tts(clean_text, lang))
                    
                    if on_start: on_start()
                    
                    # Play from memory buffer
                    import io
                    audio_buffer = io.BytesIO(audio_data)
                    pygame.mixer.music.load(audio_buffer)
                    pygame.mixer.music.set_volume(self.volume)
                    pygame.mixer.music.play()
                    
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(50)
                    
                except Exception as e:
                    print(f"Audio Error: {e}")
                finally:
                    try:
                        pygame.mixer.music.stop()
                    except: pass
                    if on_end: on_end()

        threading.Thread(target=play_thread, daemon=True).start()
