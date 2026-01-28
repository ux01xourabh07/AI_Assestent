import sys
from gui import ShipraGUI
from config import Config

def main():
    print("Initializing Shipra AI GUI...")
    Config.ensure_directories()
    
    app = ShipraGUI()
    app.mainloop()

if __name__ == "__main__":
    main()