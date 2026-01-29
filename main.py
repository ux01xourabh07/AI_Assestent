import os
import sys
from PyQt6.QtWidgets import QApplication
from gui import ShipraGUI
from config import Config

def main():
    print("Launching Shipra AI System (PyQt6)...")
    Config.ensure_directories()
    
    app = QApplication(sys.argv)
    
    print("Starting GUI...")
    window = ShipraGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()