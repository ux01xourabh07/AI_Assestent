import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, 
    QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QStyleFactory
)
from PyQt5.QtCore import (
    Qt, pyqtSignal, QThread
)
from PyQt5.QtGui import QFont, QIcon
from ai_assistant import AIAssistant

class AssistantWorker(QThread):
    """
    Worker thread to handle AI speaking without freezing the GUI.
    """
    status_changed = pyqtSignal(str)
    subtitle_received = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant
        
    def run(self):
        try:
            self.status_changed.emit("Speaking...")
            response_text = self.assistant.get_response()
            self.subtitle_received.emit(response_text)
            self.assistant.speak(response_text)
            self.status_changed.emit("Idle")
        except Exception as e:
            self.status_changed.emit(f"Error: {e}")
        self.finished.emit()

class AssistantGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Assistant")
        self.resize(600, 400)
        
        # Core
        self.ai = AIAssistant()
        self.worker = AssistantWorker(self.ai)
        self.worker.status_changed.connect(self.update_status)
        self.worker.subtitle_received.connect(self.update_subtitles)
        
        # UI Setup
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header / Status
        self.lbl_status = QLabel("Status: Idle")
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setFont(QFont("Segoe UI", 12))
        layout.addWidget(self.lbl_status)
        
        # Chat / Subtitle Area
        self.lbl_subtitle = QLabel("Welcome. Press Start to interact.")
        self.lbl_subtitle.setWordWrap(True)
        self.lbl_subtitle.setAlignment(Qt.AlignCenter)
        self.lbl_subtitle.setFont(QFont("Segoe UI", 14))
        self.lbl_subtitle.setStyleSheet("background-color: #f0f0f0; border-radius: 8px; padding: 20px; color: #333;")
        self.lbl_subtitle.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.lbl_subtitle)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.btn_start = QPushButton("Start Interaction")
        self.btn_start.setMinimumHeight(45)
        self.btn_start.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.btn_start.clicked.connect(self.trigger_ai)
        
        self.btn_quit = QPushButton("Exit")
        self.btn_quit.setMinimumHeight(45)
        self.btn_quit.setFont(QFont("Segoe UI", 11))
        self.btn_quit.clicked.connect(self.close)
        
        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_quit)
        layout.addLayout(btn_layout)

    def trigger_ai(self):
        if not self.worker.isRunning():
            self.worker.start()
            self.btn_start.setEnabled(False)

    def update_status(self, status):
        self.lbl_status.setText(f"Status: {status}")
        if status == "Idle":
            self.btn_start.setEnabled(True)
            self.btn_start.setText("Start Interaction")
        else:
            self.btn_start.setText("Processing...")

    def update_subtitles(self, text):
        self.lbl_subtitle.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion') # Standard clean look
    window = AssistantGUI()
    window.show()
    sys.exit(app.exec_())
