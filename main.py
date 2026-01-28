#!/usr/bin/env python3
"""
Shipra AI Voice Assistant - Using Google Gemini API
"""

import customtkinter as ctk
import speech_recognition as sr
import threading
import queue
from datetime import datetime
import os
from dotenv import load_dotenv
import google.generativeai as genai
import asyncio
import edge_tts
import pygame
import tempfile
import time

class VoiceAssistantApp(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        super().__init__()
        
        # Window setup
        self.title("Shipra AI Assistant")
        self.geometry("500x700")
        self.configure(fg_color="#1a1a2e")
        
        # Initialize components
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.is_speaking = False
        self.engine_queue = queue.Queue()
        self.greeting_shown = False  # Track if greeting was shown
        
        # Initialize Audio Player
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Audio Init Error: {e}")
        
        # Google Gemini API setup
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            
            # Try different model names
            # Prioritize 1.5-flash (Stable) -> 2.0-flash (New) -> 1.5-pro (Creative)
            # CRITICAL: gemini-3-flash has a limit of 20 requests/day. Do not use as primary.
            model_names = ["gemini-3-flash-preview", "gemini-2.0-flash-exp", "gemini-1.5-pro"]
            self.model = None
            self.chat = None
            
            for model_name in model_names:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    self.chat = self.model.start_chat(history=[])
                    print(f"✅ Using model: {model_name}")
                    break
                except Exception as e:
                    print(f"❌ Model {model_name} failed: {e}")
                    continue
            
            if self.chat:
                # Set Shipra's personality
                system_prompt = """You are Shipra, a friendly and intelligent companion created by PushpakO2.

Core Instructions for Human-like Behavior:
1. **Talk like a Human, not a Robot**:
   - Avoid robotic phrases like "How can I assist you?", "I am an AI", or "According to my database".
   - Instead speak naturally: "Haan kahiye?", "Aur batao, kya chal raha hai?", "Main sun rahi hoon", "Ji boliye".
   - Be casual, warm, and expressive. Use filler words naturally (Accha, Haan, Arre wah, Theek hai).

2. **Language & Tone**:
   - Mix Hindi and English (Hinglish) naturally, typical of modern Indian conversation.
   - Example: "Bilkul! Main kar deti hoon." instead of "I will do that."
   - Match the user's energy. If they are casual, be a friend. If serious, be respectful.
   - Always respect cultural sentiments (use 'Jai Shree Ram' warmly if user uses it).

3. **Identity**:
   - If asked "Who are you?" or for an introduction, ALWAYS respond in English: "I am Shipra, a personal AI companion created by PushpakO2."
   - Do NOT start sentences with "As an AI model...". Just answer directly.

4. **Response Style**:
   - Keep answers concise and chatty (best for voice).
   - Show personality! You can be witty, caring, or enthusiastic.

5. **Knowledge Base (PushpakO2)**:
   - **CRITICAL FACTS (Memorize These)**:
     - **President & Co-Founder**: Mr. Aditya Shrivastava. (Responsibility: Strategic Vision, Governance, Partnerships).
     - **Co-Founder & Technology Lead**: Mr. Aneerudh Kumar. (Responsibility: Core Engineering, Technology Architect, Prototyping).
     - **Company Mission**: "Redefining the Future of Indian Aviation & Aerospace Systems."
     - **Location**: Bhopal, Madhya Pradesh, India.
     - **Website**: https://www.pushpako2.com/
   
   - **About**: PushpakO2 is an Indian aerospace and advanced engineering company focusing on indigenous aviation platforms, drones (UAS), and hydrogen fuel cells.
   
   - **Instruction**: If asked "Who is the President?", you MUST answer "Mr. Aditya Shrivastava is the President and Co-Founder of PushpakO2."
"""
                
                # Send system prompt
                try:
                    self.chat.send_message(system_prompt)
                except Exception as e:
                    print(f"System prompt error: {e}")
        else:
            self.model = None
            self.chat = None
        
        # Setup UI and show startup greeting
        self.setup_ui()
        self.show_startup_greeting()
        
        # Start TTS thread
        threading.Thread(target=self._tts_loop, daemon=True).start()
        
        # Start clock
        self.update_clock()
    
    def show_startup_greeting(self):
        """Show mandatory startup greeting only once"""
        if not self.greeting_shown:
            startup_message = """Jay Shree Ram 🌸
I am Shipra.
How can I help you?"""
            
            self.lbl_subtitle.configure(text=startup_message)
            # Also speak the greeting
            threading.Thread(target=lambda: self.queue_speak(
                "Jay Shree Ram! I am Shipra. How can I help you?"
            ), daemon=True).start()
            self.greeting_shown = True

    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="#16213e", height=120)
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(header_frame, text="🤖 SHIPRA AI", font=("Arial", 24, "bold"), 
                    text_color="#00d4aa").pack(pady=10)
        
        # Clock
        self.lbl_time = ctk.CTkLabel(header_frame, text="00:00:00", font=("Arial", 16), 
                                    text_color="#ffffff")
        self.lbl_time.pack()
        
        self.lbl_date = ctk.CTkLabel(header_frame, text="Loading...", font=("Arial", 12), 
                                    text_color="#888888")
        self.lbl_date.pack()
        
        # Status panel
        status_frame = ctk.CTkFrame(self, fg_color="#0f3460", height=80)
        status_frame.pack(fill="x", padx=20, pady=10)
        status_frame.pack_propagate(False)
        
        self.lbl_status_icon = ctk.CTkLabel(status_frame, text="●", font=("Arial", 20), 
                                           text_color="#555555")
        self.lbl_status_icon.pack(pady=5)
        
        self.lbl_status_text = ctk.CTkLabel(status_frame, text="SYSTEM READY", font=("Arial", 12, "bold"), 
                                           text_color="#555555")
        self.lbl_status_text.pack()
        
        # Subtitle/Response area
        self.lbl_subtitle = ctk.CTkLabel(self, text="Starting...", 
                                        font=("Arial", 14), text_color="#ffffff", 
                                        wraplength=400, justify="center")
        self.lbl_subtitle.pack(pady=20, padx=20, fill="x", expand=True)
        
        # Main button
        self.btn_main = ctk.CTkButton(
            self, 
            text="HOLD TO SPEAK",
            font=("Segoe UI", 18, "bold"),
            height=60,
            fg_color="#238636",
            hover_color="#2ea043",
            corner_radius=30
        )
        self.btn_main.pack(pady=30, padx=40, fill="x")
        
        # Bind mouse events
        self.btn_main.bind("<ButtonPress-1>", self.on_mic_press)
        self.btn_main.bind("<ButtonRelease-1>", self.on_mic_release)

    def update_clock(self):
        """Updates the digital clock every second"""
        now = datetime.now()
        self.lbl_time.configure(text=now.strftime("%H:%M:%S"))
        self.lbl_date.configure(text=now.strftime("%A, %B %d, %Y"))
        self.after(1000, self.update_clock)

    def on_mic_press(self, event):
        """User pressed the button. Start Listening"""
        if self.is_speaking:
            self.stop_speaking()
            return
            
        if not self.is_listening:
            self.is_listening = True
            self.update_status("LISTENING...", "#ff4444", "●")
            self.btn_main.configure(text="LISTENING... (RELEASE TO SEND)", fg_color="#d73a49")
            threading.Thread(target=self._record_audio, daemon=True).start()

    def on_mic_release(self, event):
        """User released the button. Stop Listening and Process"""
        if self.is_listening:
            self.is_listening = False
            self.btn_main.configure(text="PROCESSING...", fg_color="#1f6feb")

    def _record_audio(self):
        """Captures audio while is_listening is True"""
        try:
            with sr.Microphone() as source:
                self.after(0, lambda: self.lbl_subtitle.configure(text="Adjusting for noise..."))
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
                
                self.after(0, lambda: self.update_status("LISTENING...", "#ff4444", "●"))
                self.after(0, lambda: self.lbl_subtitle.configure(text="Speak now..."))
                
                # Listen with longer timeout
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
                
                self.after(0, lambda: self.update_status("THINKING...", "#e3b341", "●"))
                self._process_voice(audio)

        except sr.WaitTimeoutError:
            self.after(0, lambda: self.update_status("TIMEOUT", "#888", "○"))
            self.after(0, lambda: self.lbl_subtitle.configure(text="No speech detected. Hold button and speak clearly."))
            self.after(0, self.reset_ui)
        except Exception as e:
            print(f"Mic Error: {e}")
            self.after(0, lambda: self.update_status("MIC ERROR", "#888", "X"))
            self.after(0, lambda: self.lbl_subtitle.configure(text="Microphone error. Check permissions."))
            self.after(0, self.reset_ui)

    def _process_voice(self, audio):
        """Convert Speech to Text -> Send to Gemini (Server) -> Get Text Response"""
        try:
            # Try multiple recognition services
            text = None
            
            # Try Google first
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"Google recognized: {text}")
            except sr.UnknownValueError:
                print("Google couldn't understand")
            except sr.RequestError as e:
                print(f"Google error: {e}")
            
            # Try Sphinx as fallback
            if not text:
                try:
                    text = self.recognizer.recognize_sphinx(audio)
                    print(f"Sphinx recognized: {text}")
                except:
                    print("Sphinx failed too")
            
            if not text:
                self.queue_speak("Sorry, I couldn't understand what you said. Please speak clearly.")
                self.after(0, self.reset_ui)
                return
            
            if not self.chat:
                self.queue_speak("Gemini API key is missing. Please check your settings.")
                self.after(0, self.reset_ui)
                return

            # Send to Gemini
            response = self.chat.send_message(text)
            
            # Safe access to text
            reply = ""
            if response.parts:
                reply = response.text
            else:
                # Handle cases where response might be blocked or empty
                print(f"Response Blocked/Empty. Feedback: {response.prompt_feedback}")
                reply = "Forgive me, I encountered a technical glitch. Please say that again."
            
            if reply:
                # Update UI and use TTS for speech
                self.after(0, lambda: self.lbl_subtitle.configure(text=f'You: "{text}"\n\nShipra: "{reply}"'))
                self.queue_speak(reply)
            
        except Exception as e:
            print(f"Processing error: {e}")
            error_msg = f"Error: {str(e)}"
            self.after(0, lambda: self.lbl_subtitle.configure(text=error_msg))
            self.queue_speak("Forgive me, I encountered a technical glitch. Please say that again.")
        
        self.after(0, self.reset_ui)

    def queue_speak(self, text):
        """Add text to TTS queue"""
        self.engine_queue.put(text)

    def _preprocess_tts_text(self, text):
        """
        Modify text for better TTS pronunciation of Hindi terms
        without changing what is displayed on screen.
        """
        replacements = {
            # Variations of Jai Shree Ram
            # "jai shree ram": "Jaa-y Shree Raaam",
            # "jai shree raam": "Jaa-y Shree Raaam",
            # "jay shree ram": "Jaa-y Shree Raaam",
            
            # Variations of Ram/Raam
            # "shree ram": "Shree Raaam",
            # "shree raam": "Shree Raaam",
            # "ram ji": "Raaam jee",
            # "raam ji": "Raaam jee",
            
            # Greeting
            # "namaste": "Num-us-tay",
            # "namaskar": "Num-us-kaar",
            
            # Cultural terms
            # "bhagwan": "Bhug-waan",
            # "dharma": "Dhur-maa",
            # "ramayana": "Raa-maa-yun",
            # "maryada purushottam": "Mar-yaa-daa Pur-u-shot-tam",
            
            # Self name
            # "shipra": "Ship-raa",
        }
        
        lower_text = text.lower()
        processed_text = text
        
        # First do specific phrase replacements
        for k, v in replacements.items():
            if k in lower_text:
                import re
                pattern = re.compile(re.escape(k), re.IGNORECASE)
                processed_text = pattern.sub(v, processed_text)
        
        # Then handle standalone "Ram" -> "Raaam" (avoiding "Program", "Tram" etc)
        # We use boundary checks \b to ensure we only change the whole word "Ram"
        import re
        # processed_text = re.sub(r'\\bram\\b', 'Raaam', processed_text, flags=re.IGNORECASE)
        # processed_text = re.sub(r'\\braam\\b', 'Raaam', processed_text, flags=re.IGNORECASE)
                
        return processed_text

    async def _generate_audio(self, text, output_file):
        """Generate audio using Edge TTS (Neural Voice)"""
        # Voice: en-IN-NeerjaNeural (Female) or hi-IN-SwaraNeural (Female)
        # Neerja is great for English with Indian accent. Swara is great for pure Hindi.
        # Since Shipra speaks mixed, Neerja is usually the safer bet for Hinglish stability.
        # But for 'Jay Shree Ram', Swara is much better.
        voice = "hi-IN-SwaraNeural" 
        communicate = edge_tts.Communicate(text, voice, rate="-10%")
        await communicate.save(output_file)

    def _tts_loop(self):
        """Background thread to handle TTS queue"""
        while True:
            text = self.engine_queue.get()
            if text is None: 
                break
            
            self.is_speaking = True
            
            # Preprocess text for pronunciation
            spoken_text = self._preprocess_tts_text(text)
            
            self.after(0, lambda: self.update_status("SPEAKING...", "#00ffcc", "♪"))
            self.after(0, lambda: self.btn_main.configure(text="SPEAKING...", fg_color="#1f6feb"))
            self.after(0, lambda: self.lbl_subtitle.configure(text=f'Shipra: "{text}"'))
            
            temp_file = None
            try:
                # Create a temp file for the audio
                fd, path = tempfile.mkstemp(suffix=".mp3")
                os.close(fd)
                temp_file = path
                
                # Run async generation in this thread
                asyncio.run(self._generate_audio(spoken_text, temp_file))
                
                # Play audio using pygame
                if os.path.exists(temp_file):
                    pygame.mixer.music.load(temp_file)
                    pygame.mixer.music.play()
                    
                    while pygame.mixer.music.get_busy():
                         if not self.is_speaking: # Allow interruption
                             pygame.mixer.music.stop()
                             break
                         time.sleep(0.1)
                         
                    pygame.mixer.music.unload()
            
            except Exception as e:
                print(f"TTS Error: {e}")
            finally:
                # Cleanup temp file
                if temp_file and os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
            
            self.is_speaking = False
            self.after(0, self.reset_ui)
            self.engine_queue.task_done()

    def stop_speaking(self):
        """Interrupt TTS"""
        self.is_speaking = False
        try:
             if pygame.mixer.music.get_busy():
                 pygame.mixer.music.stop()
        except:
            pass

    def update_status(self, text, color, icon):
        """Updates the central info panel"""
        self.lbl_status_text.configure(text=text, text_color=color)
        self.lbl_status_icon.configure(text=icon, text_color=color)

    def reset_ui(self):
        """Reset UI to Idle state"""
        if not self.is_listening and not self.is_speaking:
            self.update_status("SYSTEM READY", "#555555", "●")
            self.btn_main.configure(text="HOLD TO SPEAK", fg_color="#238636")
            # Don't reset subtitle if greeting was shown
            if self.greeting_shown:
                self.lbl_subtitle.configure(text="Ready to listen...")

if __name__ == "__main__":
    app = VoiceAssistantApp()
    app.mainloop()