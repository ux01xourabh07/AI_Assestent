#!/usr/bin/env python3
"""
Gemini AI Voice Assistant - Complete GUI Application
"""

import customtkinter as ctk
import speech_recognition as sr
import pyttsx3
import threading
import queue
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

class VoiceAssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("Gemini AI Assistant")
        self.geometry("500x700")
        self.configure(fg_color="#1a1a2e")
        
        # Initialize components
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.is_speaking = False
        self.engine_queue = queue.Queue()
        self.messages = [{"role": "system", "content": "You are a helpful AI assistant. Keep responses concise."}]
        
        # Gemini API setup
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
        else:
            self.client = None
        self.model_name = "gemini-3-flash-preview"
        
        # Setup UI
        self.setup_ui()
        
        # Start TTS thread
        threading.Thread(target=self._tts_loop, daemon=True).start()
        
        # Start clock
        self.update_clock()

    def setup_ui(self):
        """Setup the user interface"""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="#16213e", height=120)
        header_frame.pack(fill="x", padx=20, pady=20)
        header_frame.pack_propagate(False)
        
        ctk.CTkLabel(header_frame, text="🤖 GEMINI AI", font=("Arial", 24, "bold"), 
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
        self.lbl_subtitle = ctk.CTkLabel(self, text="Hold the button and speak", 
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
            self.after(0, lambda: self.lbl_subtitle.configure(text=f"Microphone error. Check permissions."))
            self.after(0, self.reset_ui)

    def _process_voice(self, audio):
        """Convert Speech to Text -> Send to Gemini -> Get Text Response"""
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
            
            if not self.client:
                self.queue_speak("Gemini API key is missing. Please check your settings.")
                self.after(0, self.reset_ui)
                return

            self.messages.append({"role": "user", "content": text})
            
            # Simple Gemini API call
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=self.messages
            )
            
            # Get text response
            reply = response.choices[0].message.content
            if reply:
                self.messages.append({"role": "assistant", "content": reply})
                
                # Update UI and use TTS for speech
                self.after(0, lambda: self.lbl_subtitle.configure(text=f'You: "{text}"\n\nAI: "{reply}"'))
                self.queue_speak(reply)
            
        except Exception as e:
            print(f"Processing error: {e}")
            self.queue_speak("I encountered a technical error. Please try again.")
        
        self.after(0, self.reset_ui)

    def queue_speak(self, text):
        """Add text to TTS queue"""
        self.engine_queue.put(text)

    def _tts_loop(self):
        """Background thread to handle TTS queue"""
        while True:
            text = self.engine_queue.get()
            if text is None: 
                break
            
            self.is_speaking = True
            
            self.after(0, lambda: self.update_status("SPEAKING...", "#00ffcc", "♪"))
            self.after(0, lambda: self.btn_main.configure(text="SPEAKING...", fg_color="#1f6feb"))
            self.after(0, lambda: self.lbl_subtitle.configure(text=f'AI: "{text}"'))
            
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 160)
                voices = engine.getProperty('voices')
                for v in voices:
                    if "zira" in v.name.lower() or "female" in v.name.lower():
                        engine.setProperty('voice', v.id)
                        break
                
                engine.say(text)
                engine.runAndWait()
                engine.stop()
                del engine
            except Exception as e:
                print(f"TTS Error: {e}")
            
            self.is_speaking = False
            self.after(0, self.reset_ui)
            self.engine_queue.task_done()

    def stop_speaking(self):
        """Interrupt TTS"""
        self.is_speaking = False

    def update_status(self, text, color, icon):
        """Updates the central info panel"""
        self.lbl_status_text.configure(text=text, text_color=color)
        self.lbl_status_icon.configure(text=icon, text_color=color)

    def reset_ui(self):
        """Reset UI to Idle state"""
        if not self.is_listening and not self.is_speaking:
            self.update_status("SYSTEM READY", "#555555", "●")
            self.btn_main.configure(text="HOLD TO SPEAK", fg_color="#238636")

if __name__ == "__main__":
    app = VoiceAssistantApp()
    app.mainloop()