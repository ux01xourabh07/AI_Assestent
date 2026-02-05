
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
RVC_AVAILABLE = False
try:
    from rvc_python.infer import infer_file
    RVC_AVAILABLE = True
    print("[Audio] RVC Library found.")
except ImportError:
    print("[Audio] RVC Library NOT found (Voice Conversion disabled).")

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

        # Voice Settings
        self.voice = "en-IN-NeerjaNeural"  # Default Indian English Female
        self.rate = "+0%"
        self.volume = "+0%"
        self.pitch = "+0Hz"
        
        # RVC Settings
        self.rvc_model_path = None
        self.rvc_index_path = None
        self.check_for_rvc_model()

    def check_for_rvc_model(self):
        """Scans 'models' directory for .pth files."""
        if not RVC_AVAILABLE: return
        
        models_dir = os.path.join(os.getcwd(), "models")
        pth_files = glob.glob(os.path.join(models_dir, "*.pth"))
        
        if pth_files:
            self.rvc_model_path = pth_files[0]
            print(f"[Audio] RVC Model found: {os.path.basename(self.rvc_model_path)}")
            # Check for index
            base_name = os.path.splitext(self.rvc_model_path)[0]
            if os.path.exists(base_name + ".index"):
                self.rvc_index_path = base_name + ".index"
        else:
            print("[Audio] No RVC model (.pth) found in 'models/'. Using standard TTS.")

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
        """Generates and plays TTS audio (with optional RVC)."""
        if not text: return
        
        clean_text = self.normalize_text(text)
        print(f"\n[Shipra] RESPONSE: {clean_text}")
        
        if on_start: on_start()
        
        tts_file = "response_tts.mp3"
        final_file = "response_final.wav"
        
        # 1. Generate TTS
        asyncio.run(self._generate_edge_tts(clean_text, tts_file))
        
        # 2. Apply RVC (if available)
        if self.rvc_model_path:
            print(f"[Audio] Applying RVC ({os.path.basename(self.rvc_model_path)})...")
            try:
                infer_file(
                    input_path=tts_file,
                    model_path=self.rvc_model_path,
                    index_path=self.rvc_index_path,
                    device="cpu", # Assume CPU for safety, 'cuda:0' if GPU available
                    f0_method="rmvpe",
                    f0_up_key=0, 
                    opt_path=final_file
                )
                self._play_audio(final_file)
            except Exception as e:
                print(f"[Audio] RVC Failed: {e}. Falling back to TTS.")
                self._play_audio(tts_file)
        else:
            self._play_audio(tts_file)
        
        if on_end: on_end()

    async def _generate_edge_tts(self, text, filename):
        # Use Indian accent with decreased pitch and increased speed
        communicate = edge_tts.Communicate(
            text, 
            self.voice, 
            rate="+25%",  # Increase speed by 25%
            volume=self.volume, 
            pitch="-10%"  # Decrease pitch by 10%
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
