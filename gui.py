
import sys
import threading
import time
import math
import random
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTextEdit, QLineEdit, QPushButton, QLabel, QSlider, QFrame
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject, QSize
from PyQt6.QtGui import QFont, QColor, QPainter, QBrush, QPen, QIcon

from systems import Systems
from config import Config

# --- Styles ---
DARK_STYLESHEET = """
QMainWindow {
    background-color: #0d0d0d;
}
QWidget {
    color: #ffffff;
    font-family: 'Segoe UI', 'Roboto', sans-serif;
    font-size: 14px;
}
QTextEdit {
    background-color: #1a1a1a;
    border: 1px solid #333;
    border-radius: 10px;
    padding: 10px;
    font-size: 14px;
}
QLineEdit {
    background-color: #262626;
    border: 1px solid #444;
    border-radius: 20px;
    padding: 10px 15px;
    font-size: 14px;
    color: white;
}
QPushButton {
    background-color: #1f6feb;
    border-radius: 20px;
    padding: 10px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #3b82f6;
}
QPushButton#MicBtn {
    background-color: #2ea043; /* Green */
    font-size: 16px;
    border-radius: 25px;
}
QPushButton#MicBtn:checked {
    background-color: #da3633; /* Red */
}
QLabel#HeaderTime {
    font-size: 48px;
    font-weight: bold;
    color: #ffffff;
}
QLabel#HeaderDate {
    font-size: 18px;
    color: #888888;
}
QLabel#StatusLabel {
    font-size: 16px;
    color: #00ff00;
}
"""

# --- Visualizer Widget ---
class AudioVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(300)
        self.is_speaking = False
        self.phase = 0.0
        self.amplitude = 10
        
        # 60 FPS Animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16) 

    def set_speaking(self, active):
        self.is_speaking = active

    def update_animation(self):
        if self.is_speaking:
            self.phase += 0.2
            self.amplitude = random.randint(20, 60)
        else:
            self.phase += 0.05
            self.amplitude = 5 + math.sin(self.phase) * 2
        self.update() # Trigger paintEvent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        cx, cy = w / 2, h / 2
        
        # Base Ring
        pen = QPen(QColor("#00BFFF"))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        base_radius = 120 + math.sin(self.phase * 0.5) * 5
        painter.drawEllipse(int(cx - base_radius), int(cy - base_radius), int(base_radius * 2), int(base_radius * 2))

        # Core
        painter.setBrush(QBrush(QColor("#000000")))
        painter.drawEllipse(int(cx - 50), int(cy - 50), 100, 100)

        # Wave
        path_points = []
        num_points = 100
        angle_step = (2 * math.pi) / num_points
        
        for i in range(num_points + 1):
            angle = i * angle_step
            wave = math.sin(angle * 6 + self.phase) * self.amplitude
            r = 100 + wave
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            
            if i == 0:
                painter.setPen(QPen(QColor("#00BFFF"), 2))
                # For polygon, we don't strictly need moveTo, but good for paths
            
            # We are just drawing a polygon for simplicity
            # For a proper smooth wave, QPainterPath is better, but this is fast.
            # Let's use drawPolyline or drawPolygon
            pass # Logic moved to QPolygonF if needed, simpler to just draw circle-ish

        # Simple particle effect for "Wave"
        painter.setPen(QPen(QColor("#00BFFF"), 4))
        for i in range(num_points):
            angle = i * angle_step
            wave_r = 100 + math.sin(angle * 8 + self.phase) * self.amplitude
            x = cx + wave_r * math.cos(angle)
            y = cy + wave_r * math.sin(angle)
            painter.drawPoint(int(x), int(y))


# --- Worker Threads ---

class SystemLoader(QThread):
    finished = pyqtSignal()
    
    def run(self):
        Systems.get_brain()
        Systems.get_audio()
        self.finished.emit()

class BrainWorker(QThread):
    response_ready = pyqtSignal(str, str) # text, source
    
    def __init__(self, text):
        super().__init__()
        self.text = text
        
    def run(self):
        brain = Systems.get_brain()
        try:
            response = brain.chat(self.text)
            self.response_ready.emit(response, "Shipra")
        except Exception as e:
            self.response_ready.emit(str(e), "Error")

class ListenWorker(QThread):
    text_heard = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.paused = False
        
    def run(self):
        audio = Systems.get_audio()
        while self.running:
            if self.paused:
                time.sleep(0.5)
                continue
                
            try:
                text = audio.listen()
                if text:
                    # Auto-pause immediately to prevent re-entry/race conditions
                    self.paused = True 
                    self.text_heard.emit(text)
            except Exception:
                pass
                
    def stop(self):
        self.running = False
        
class SpeakWorker(QThread):
    finished = pyqtSignal()
    started = pyqtSignal()
    
    def __init__(self, text):
        super().__init__()
        self.text = text
        
    def run(self):
        audio = Systems.get_audio()
        self.started.emit()
        # Blocking call to audio.speak is fine in a thread
        # We need to bridge the callbacks manually or just rely on blocking
        # audio.speak launches its OWN thread in current impl.
        # We should call the 'internal' synchronous generate or just wrap the existing method.
        # For compatibility with audio.py:
        
        # We use a trick: lock primitive or sleep loop to wait
        # But audio.speak is threaded. Let's make a blocking version in audio.py later?
        # For now, we just call it. But we want to know when it starts/ends for Visualizer.
        
        event = threading.Event()
        
        def on_start():
            self.started.emit()
            
        def on_end():
            event.set()
            
        audio.speak(self.text, on_start=on_start, on_end=on_end)
        event.wait() # Block this QThread until audio finishes
        self.finished.emit()


# --- Main Window ---

class ShipraGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shipra AI Assistant (PyQt6)")
        self.resize(1000, 700)
        self.setWindowIcon(QIcon("icon.png")) # Optional
        
        # State
        self.is_ready = False
        self.listen_thread = None
        self.speak_thread = None
        
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # 1. Header
        self.setup_header()
        
        # 2. Visualizer
        self.visualizer = AudioVisualizer()
        self.layout.addWidget(self.visualizer, 1) # Stretch
        
        # 3. Chat Area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMinimumHeight(150)
        self.layout.addWidget(self.chat_display)
        
        # 4. Input Area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your message here...")
        self.input_field.returnPressed.connect(self.on_send_click)
        
        self.send_btn = QPushButton("SEND")
        self.send_btn.clicked.connect(self.on_send_click)
        self.send_btn.setFixedWidth(100)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_btn)
        self.layout.addLayout(input_layout)
        
        # 5. Controls
        control_layout = QHBoxLayout()
        
        self.volume_label = QLabel("Volume: 70%")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        self.volume_slider.setFixedWidth(200)
        self.volume_slider.valueChanged.connect(self.on_volume_change)
        
        self.status_label = QLabel("Initializing...", objectName="StatusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.mic_btn = QPushButton("MIC ON", objectName="MicBtn")
        self.mic_btn.setCheckable(True)
        self.mic_btn.setChecked(False) # Not muted
        self.mic_btn.setFixedWidth(150)
        self.mic_btn.setFixedHeight(50)
        self.mic_btn.clicked.connect(self.toggle_mic)
        
        
        # Voice Controls
        voice_layout = QVBoxLayout()
        voice_layout.setContentsMargins(0, 0, 0, 0)
        
        # Pitch
        pitch_row = QHBoxLayout()
        self.pitch_label = QLabel("Pitch: 0 Hz")
        self.pitch_slider = QSlider(Qt.Orientation.Horizontal)
        self.pitch_slider.setRange(-50, 50)
        self.pitch_slider.setValue(0)
        self.pitch_slider.setFixedWidth(150)
        self.pitch_slider.valueChanged.connect(self.on_voice_params_change)
        pitch_row.addWidget(QLabel("Pitch:"))
        pitch_row.addWidget(self.pitch_slider)
        pitch_row.addWidget(self.pitch_label)
        
        # Rate
        rate_row = QHBoxLayout()
        self.rate_label = QLabel("Speed: +10 %")
        self.rate_slider = QSlider(Qt.Orientation.Horizontal)
        self.rate_slider.setRange(-50, 50)
        self.rate_slider.setValue(10)
        self.rate_slider.setFixedWidth(150)
        self.rate_slider.valueChanged.connect(self.on_voice_params_change)
        rate_row.addWidget(QLabel("Speed:"))
        rate_row.addWidget(self.rate_slider)
        rate_row.addWidget(self.rate_label)
        
        voice_layout.addLayout(pitch_row)
        voice_layout.addLayout(rate_row)
        
        control_layout.addLayout(voice_layout)
        control_layout.addSpacing(20)

        control_layout.addWidget(QLabel("Volume:"))
        control_layout.addWidget(self.volume_slider)
        control_layout.addWidget(self.volume_label)
        control_layout.addStretch()
        control_layout.addWidget(self.status_label)
        control_layout.addStretch()
        control_layout.addWidget(self.mic_btn)
        
        self.layout.addLayout(control_layout)
        
        # Styles
        self.setStyleSheet(DARK_STYLESHEET)
        
        # Init Timer for clock
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()
        
        # Start Loading
        self.start_initialization()

    def setup_header(self):
        header = QFrame()
        h_layout = QVBoxLayout(header)
        h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.time_lbl = QLabel("00:00", objectName="HeaderTime")
        self.time_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.date_lbl = QLabel("Date", objectName="HeaderDate")
        self.date_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        h_layout.addWidget(self.time_lbl)
        h_layout.addWidget(self.date_lbl)
        self.layout.addWidget(header)

    def update_time(self):
        now = datetime.now()
        self.time_lbl.setText(now.strftime("%H:%M"))
        self.date_lbl.setText(now.strftime("%A, %d %B %Y"))

    def on_volume_change(self, value):
        self.volume_label.setText(f"Volume: {value}%")
        if self.is_ready:
            Systems.get_audio().set_volume(value / 100.0)

    def on_voice_params_change(self):
        pitch = self.pitch_slider.value()
        rate = self.rate_slider.value()
        
        self.pitch_label.setText(f"Pitch: {pitch} Hz")
        self.rate_label.setText(f"Speed: {rate:+d} %")
        
        if self.is_ready:
            Systems.get_audio().set_voice_params(pitch, rate)

    def toggle_mic(self):
        is_muted = self.mic_btn.isChecked()
        if is_muted:
            self.mic_btn.setText("MIC OFF")
            self.status_label.setText("Microphone Off")
            self.status_label.setStyleSheet("color: red;")
            if self.listen_thread: self.listen_thread.paused = True
        else:
            self.mic_btn.setText("MIC ON")
            self.status_label.setText("Listening...")
            self.status_label.setStyleSheet("color: #00ff00;")
            if self.listen_thread: self.listen_thread.paused = False

    def start_initialization(self):
        self.status_label.setText("Loading AI Systems...")
        self.status_label.setStyleSheet("color: orange;")
        self.loader = SystemLoader()
        self.loader.finished.connect(self.on_systems_loaded)
        self.loader.start()

    def on_systems_loaded(self):
        self.is_ready = True
        self.status_label.setText("Systems Ready. Listening...")
        self.status_label.setStyleSheet("color: #00ff00;")
        self.add_message("System", "AI Models Loaded. Ready!")
        
        # Start Listen Thread
        self.listen_thread = ListenWorker()
        self.listen_thread.paused = True # Start paused to speak intro first
        self.listen_thread.text_heard.connect(self.process_input)
        self.listen_thread.start()
        
        # Initial Greeting (Female Persona)
        intro = "Jay Shree Ram! Main PushpakO2 dwara banai gayi ek smart AI Assistant hoon. Main apki kya madad kar sakti hoon?"
        self.add_message("Shipra", intro)
        self.speak(intro)

    def add_message(self, sender, text):
        color = "#1f6feb" if sender == "User" else "#2ea043"
        if sender == "System": color = "orange"
        
        html = f'<div style="margin-bottom: 10px;"><span style="color: {color}; font-weight: bold;">{sender}:</span> <span style="color: #ddd;">{text}</span></div>'
        self.chat_display.append(html)
        # Scroll to bottom
        sb = self.chat_display.verticalScrollBar()
        sb.setValue(sb.maximum())

    def on_send_click(self):
        text = self.input_field.text().strip()
        if text:
            self.input_field.clear()
            self.process_input(text)

    def process_input(self, text):
        if not text: return
        
        # Pause Listening so we don't hear ourselves
        if self.listen_thread: self.listen_thread.paused = True
        
        self.status_label.setText("Thinking...")
        self.status_label.setStyleSheet("color: cyan;")
        self.add_message("User", text)
        
        self.brain_worker = BrainWorker(text)
        self.brain_worker.response_ready.connect(self.on_brain_response)
        self.brain_worker.start()

    def on_brain_response(self, response, source):
        self.add_message("Shipra", response)
        self.speak(response)

    def speak(self, text):
        self.status_label.setText("Speaking...")
        self.status_label.setStyleSheet("color: violet;")
        
        self.speak_thread = SpeakWorker(text)
        self.speak_thread.started.connect(lambda: self.visualizer.set_speaking(True))
        self.speak_thread.finished.connect(self.on_speak_finished)
        self.speak_thread.start()

    def on_speak_finished(self):
        self.visualizer.set_speaking(False)
        # Resume listening if not manually muted
        if not self.mic_btn.isChecked():
            self.status_label.setText("Listening...")
            self.status_label.setStyleSheet("color: #00ff00;")
            self.listen_thread.paused = False # CONTINUOUS MODE ENABLED
        else:
            self.status_label.setText("Microphone Off")
            self.status_label.setStyleSheet("color: red;")

    def closeEvent(self, event):
        if self.listen_thread: self.listen_thread.stop()
        event.accept()

