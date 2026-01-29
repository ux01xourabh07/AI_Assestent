import asyncio
import os
import threading
import io
import pygame
import speech_recognition as sr
import numpy as np
import edge_tts
from langdetect import detect

# Note: 'whisper' import removed to rely on lightweight Google Speech Recognition
# for faster response and lower resource usage, as requested.

class ShipraAudio:
    def __init__(self):
        # STT Setup
        self.recognizer = sr.Recognizer()
        
        # KEY SETTINGS FOR "CATCHING VOICE"
        self.recognizer.energy_threshold = 300  # Lower default (was 400) to catch quieter voices
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.pause_threshold = 0.8  # Wait 0.8s of silence before considering phrase complete
        self.recognizer.phrase_threshold = 0.3  # Minimum length of a phrase
        self.recognizer.non_speaking_duration = 0.5 

        print("--------------------------------------------------")
        print("[Audio] Initializing Audio System...")
        print(f"[Audio] Energy Threshold: {self.recognizer.energy_threshold} (Dynamic: {self.recognizer.dynamic_energy_threshold})")
        print("[Audio] Using Google Speech Recognition (Fast Mode)")
        print("--------------------------------------------------")

        # Audio Output Setup
        try:
            pygame.mixer.init()
            print("[Audio] Pygame Mixer Initialized.")
        except Exception as e:
            print(f"[Audio] CRITICAL WARNING: Audio Output Init Failed: {e}")
            
        self.volume = 1.0
        self.lock = threading.Lock()

    def set_volume(self, volume):
        """Sets the volume for the audio output."""
        try:
            self.volume = float(volume)
            # Apply immediately if music is playing
            if pygame.mixer.get_init():
                pygame.mixer.music.set_volume(self.volume)
            print(f"[Audio] Volume set to: {self.volume}")
        except Exception as e:
            print(f"[Audio] Error setting volume: {e}")

    def normalize_text(self, text):
        replacements = {
            "AI": "Artificial Intelligence",
            "API": "A P I",
            "Shipra": "Ship-raa",
            "OK": "Okay",
            "ok": "okay",
            "OKAY": "Okay"
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
        Robust listening loop using SpeechRecognition.
        """
        with sr.Microphone() as source:
            print("\n[Audio] Adjusting for ambient noise... (Please wait)")
            self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
            print(f"[Audio] Threshold adjusted to: {self.recognizer.energy_threshold}")
            print("[Audio] LISTENING... (Speak now)")
            
            try:
                # Listen with timeouts
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("[Audio] Processing voice data...")
                
                try:
                    # Recognize
                    text = self.recognizer.recognize_google(audio)
                    print(f"[Audio] USER SAID: '{text}'")
                    return text
                except sr.UnknownValueError:
                    print("[Audio] Creating transcript... (Could not understand audio)")
                    return None
                except sr.RequestError as e:
                    print(f"[Audio] API Error (Google Speech): {e}")
                    return None
                    
            except sr.WaitTimeoutError:
                print("[Audio] Timeout: No speech detected.")
                return None
            except Exception as e:
                print(f"[Audio] Listening Error: {e}")
                return None

    async def _generate_edge_tts(self, text, lang):
        """Generate TTS to memory buffer."""
        # Multi-lingual voice support
        voice = "hi-IN-MadhurNeural" # Defaults to a voice good for Hinglish
        if lang == "en":
             # Use a clear English voice if purely English is detected/forced
             voice = "en-US-AriaNeural"

        print(f"[Audio] Generating TTS (Lang: {lang}, Voice: {voice})...")
        
        try:
            communicate = edge_tts.Communicate(text, voice, rate="+0%")
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data
        except Exception as e:
            print(f"[Audio] TTS Generation Failed: {e}")
            return None

    def speak(self, text, on_start=None, on_end=None):
        def play_thread():
            with self.lock:
                try:
                    lang = self.detect_language(text)
                    clean_text = self.normalize_text(text)
                    
                    print(f"\n[Shipra] SPEAKING ({lang}): {clean_text}")
                    
                    # Generate audio to memory
                    audio_data = asyncio.run(self._generate_edge_tts(clean_text, lang))
                    
                    if not audio_data:
                        print("[Audio] Error: No audio data generated.")
                        if on_end: on_end()
                        return

                    if on_start: on_start()
                    
                    # Play from memory buffer
                    pygame.mixer.music.load(io.BytesIO(audio_data))
                    pygame.mixer.music.set_volume(self.volume)
                    pygame.mixer.music.play()
                    
                    while pygame.mixer.music.get_busy():
                        pygame.time.wait(100)
                        
                except Exception as e:
                    print(f"[Audio] Playback Error: {e}")
                finally:
                    try:
                        pygame.mixer.music.unload()
                    except: pass
                    print("[Audio] Finished speaking.")
                    if on_end: on_end()

        threading.Thread(target=play_thread, daemon=True).start()
