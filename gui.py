import customtkinter as ctk
import tkinter as tk
from datetime import datetime
import threading
import math
import random
import pygame
from systems import Systems
from config import Config

# Theme Settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class GUIConfig:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    RING_COLOR_1 = "#00BFFF" # Deep Sky Blue
    RING_COLOR_2 = "#000000" # Black/Dark
    TEXT_COLOR = "#FFFFFF"

class Visualizer(ctk.CTkCanvas):
    def __init__(self, master, width, height, **kwargs):
        super().__init__(master, width=width, height=height, bg="#0d0d0d", highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.center_x = width // 2
        self.center_y = height // 2
        self.is_speaking = False
        self.phase = 0
        self.amplitude = 10
        self.animation_id = None
        
        # Initial draw
        self.animate()

    def set_speaking(self, speaking):
        self.is_speaking = speaking

    def animate(self):
        self.delete("all")
        
        # Base Ring (Static/Breathing Outer)
        radius_base = 150 + math.sin(self.phase * 0.05) * 10
        self.create_oval(
            self.center_x - radius_base, self.center_y - radius_base,
            self.center_x + radius_base, self.center_y + radius_base,
            outline=GUIConfig.RING_COLOR_1, width=3
        )

        # Dynamic Wave Inner
        points = []
        num_points = 100
        angle_step = (2 * math.pi) / num_points
        
        current_amp = self.amplitude
        if self.is_speaking:
            current_amp = random.randint(20, 50) # Chaotic when speaking
            self.phase += 0.5
        else:
            current_amp = 8 # Calm breathing
            self.phase += 0.1

        for i in range(num_points + 1): # +1 to close loop
            angle = i * angle_step
            # Wave formula
            wave = math.sin(angle * 6 + self.phase) * current_amp
            r = 130 + wave
            x = self.center_x + r * math.cos(angle)
            y = self.center_y + r * math.sin(angle)
            points.append(x)
            points.append(y)

        self.create_polygon(points, outline=GUIConfig.RING_COLOR_1, fill="", width=4, smooth=True)
        
        # Inner Core
        core_r = 60
        self.create_oval(
            self.center_x - core_r, self.center_y - core_r,
            self.center_x + core_r, self.center_y + core_r,
            fill=GUIConfig.RING_COLOR_2, outline=GUIConfig.RING_COLOR_1
        )

        self.animation_id = self.after(50, self.animate)

class ShipraGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Shipra AI Assistant (Voice Mode)")
        self.geometry(f"{GUIConfig.WINDOW_WIDTH}x{GUIConfig.WINDOW_HEIGHT}")
        self.configure(fg_color="#0d0d0d") # Very dark bg

        # Components (Initialized asynchronously)
        self.brain = None
        self.audio = None
        
        # State
        self.is_processing = False 
        self.is_muted = False
        self.is_running = True
        self.is_ready = False  # New flag

        self._init_ui()
        self._update_time()
        
        # Start Initialization in Background
        self.after(100, self.start_initialization)

    def start_initialization(self):
        """Loads heavy systems in background so GUI doesn't freeze."""
        threading.Thread(target=self._load_systems, daemon=True).start()

    def _load_systems(self):
        self.after(0, lambda: self.status_label.configure(text="Initializing AI Systems... (Please Wait)", text_color="orange"))
        
        # Load Systems (This triggers the lazy imports)
        self.brain = Systems.get_brain()
        self.audio = Systems.get_audio()
        
        self.is_ready = True
        self.after(0, lambda: self.status_label.configure(text="System Ready. Listening...", text_color="#00FF00"))
        self.after(0, lambda: self.chat_display.insert("end", "System: AI Models Loaded. Ready!\n"))
        
        # Speak Startup Intro (User Request)
        intro_text = "Jay Shree Ram! Main PushpakO2 dwara banaya gaya ek smart AI Assistant hoon. Main apki kya madad kar sakta hoon?"
        self.after(100, lambda: self.add_message(intro_text, "Shipra"))
        threading.Thread(target=lambda: self.audio.speak(
            intro_text, 
            on_start=lambda: self.visualizer.set_speaking(True),
            on_end=lambda: self._on_speaking_finished()
        ), daemon=True).start()
        
        # Start Listening Loop
        self.start_continuous_listening()

    def _init_ui(self):
        # Grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) # Date/Time
        self.grid_rowconfigure(1, weight=1) # Visualizer
        self.grid_rowconfigure(2, weight=0) # Chat Box (Log)
        self.grid_rowconfigure(3, weight=0) # Controls

        # 1. Header (Date Time)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, pady=20, sticky="ew")
        
        self.time_label = ctk.CTkLabel(
            self.header_frame, text="00:00", 
            font=("Roboto Medium", 64), text_color=GUIConfig.TEXT_COLOR
        )
        self.time_label.pack(pady=(20, 0))
        
        self.date_label = ctk.CTkLabel(
            self.header_frame, text="Monday, 01 January", 
            font=("Roboto", 18), text_color="gray"
        )
        self.date_label.pack()

        # 2. Visualizer
        self.visualizer = Visualizer(self, width=900, height=450)
        self.visualizer.grid(row=1, column=0, padx=20, pady=20)

        # 3. Status / Chat Log
        self.chat_display = ctk.CTkTextbox(
            self, height=80, corner_radius=10, 
            fg_color="#1a1a1a", text_color="#eee", font=("Roboto", 14)
        )
        self.chat_display.grid(row=2, column=0, padx=50, pady=(0, 10), sticky="ew")
        self.chat_display.insert("0.0", "System: Voice Mode Initialized. Listening...\n")
        self.chat_display.configure(state="disabled")

        # 3.5 Text Input Area
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=3, column=0, padx=50, pady=(0, 10), sticky="ew")
        
        self.msg_entry = ctk.CTkEntry(
            self.input_frame, placeholder_text="Type your message here...",
            font=("Arial", 14), height=40
        )
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.msg_entry.bind("<Return>", self.on_send_press)
        
        self.send_btn = ctk.CTkButton(
            self.input_frame, text="SEND", width=100, height=40,
            font=("Arial", 12, "bold"), fg_color="#1f6feb",
            command=self.on_send_press
        )
        self.send_btn.pack(side="right")
        
        # 4. Controls (Volume & Mute)
        self.control_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.control_frame.grid(row=4, column=0, pady=20)
        
        self.status_label = ctk.CTkLabel(
            self.control_frame, text="Listening...", 
            font=("Arial", 16), text_color="#00FF00"
        )
        self.status_label.pack(pady=(0, 10))

        # Volume Control
        self.volume_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        self.volume_frame.pack(pady=(0, 10))
        
        ctk.CTkLabel(self.volume_frame, text="Volume:", font=("Arial", 14)).pack(side="left", padx=(0, 10))
        
        self.volume_slider = ctk.CTkSlider(
            self.volume_frame, from_=0, to=1, number_of_steps=10,
            width=200, command=self.on_volume_change
        )
        self.volume_slider.set(0.7)  # Default volume
        self.volume_slider.pack(side="left", padx=(0, 10))
        
        self.volume_label = ctk.CTkLabel(self.volume_frame, text="70%", font=("Arial", 12))
        self.volume_label.pack(side="left")

        self.mic_btn = ctk.CTkButton(
            self.control_frame, text="MIC ON", width=200, height=50, 
            corner_radius=25, fg_color="green", hover_color="#006400",
            font=("Arial", 18, "bold"), command=self.toggle_mic
        )
        self.mic_btn.pack()

    def _update_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%A, %d %B %Y")
        
        self.time_label.configure(text=current_time)
        self.date_label.configure(text=current_date)
        
        self.after(1000, self._update_time)

    def on_volume_change(self, value):
        """Handle volume slider changes."""
        volume_percent = int(value * 100)
        self.volume_label.configure(text=f"{volume_percent}%")
        if self.audio:
            self.audio.set_volume(value)

    def toggle_mic(self):
        if not self.is_ready: return
        self.is_muted = not self.is_muted # Reusing is_muted flag as is_mic_off
        
        if self.is_muted: # Mic OFF
            self.mic_btn.configure(text="MIC OFF", fg_color="red", hover_color="#8B0000")
            self.status_label.configure(text="Microphone Off", text_color="red")
            self.visualizer.configure(bg="#1a0505") # Reddish tint
            # Optional: Stop Audio output too if desired, but user said "Mic Off"
            # self.audio.set_volume(0) 
        else: # Mic ON
            self.mic_btn.configure(text="MIC ON", fg_color="green", hover_color="#006400")
            self.status_label.configure(text="Listening...", text_color="#00FF00")
            self.visualizer.configure(bg="#0d0d0d") # Normal
            # self.audio.set_volume(self.volume_slider.get())

    def on_send_press(self, event=None):
        """Handle Manual Text Submission"""
        if not self.is_ready: return
        text = self.msg_entry.get().strip()
        if text:
            self.msg_entry.delete(0, "end")
            self.process_input(text)

    def add_message(self, text, sender="User"):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", f"\n{sender}: {text}\n")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def start_continuous_listening(self):
        threading.Thread(target=self._listening_loop, daemon=True).start()

    def _listening_loop(self):
        print("Starting continuous listening loop")
        while self.is_running:
            if not self.is_ready or self.is_muted or self.is_processing:
                pygame.time.wait(300)
                continue

            try:
                text = self.audio.listen()
                
                if text and len(text.strip()) > 0:
                    print(f"Heard: {text}")
                    self.process_input(text)
                    
                    # Wait for processing to complete
                    while self.is_processing and self.is_running:
                        pygame.time.wait(100)
                else:
                    # Short pause when no input detected
                    pygame.time.wait(100)
                    
            except Exception as e:
                print(f"Listening error: {e}")
                pygame.time.wait(500)
            
    def process_input(self, text):
        if not text: return
        
        self.is_processing = True
        self.after(0, lambda: self.status_label.configure(text="Thinking...", text_color="yellow"))
        self.after(0, lambda: self.add_message(text, "User"))
        
        # Run AI in thread
        threading.Thread(target=self._run_brain, args=(text,), daemon=True).start()

    def _run_brain(self, text):
        try:
            response = self.brain.chat(text)
            
            # Update GUI safely
            self.after(0, lambda: self.add_message(response, "Shipra"))
            self.after(0, lambda: self.status_label.configure(text="Speaking...", text_color="cyan"))
            
            # Speak (Blocking-ish call in thread, but good)
            self.audio.speak(
                response, 
                on_start=lambda: self.visualizer.set_speaking(True),
                on_end=lambda: self._on_speaking_finished()
            )
            
        except Exception as e:
            self.after(0, lambda: self.add_message(f"Error: {e}", "System"))
            self._on_speaking_finished()

    def _on_speaking_finished(self):
        self.visualizer.set_speaking(False)
        self.is_processing = False
        # Reset Status
        if not self.is_muted:
            self.after(0, lambda: self.status_label.configure(text="Listening...", text_color="#00FF00"))
        else:
            self.after(0, lambda: self.status_label.configure(text="Microphone Muted", text_color="red"))

    def on_closing(self):
        self.is_running = False
        self.destroy()

if __name__ == "__main__":
    app = ShipraGUI()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
