import os
import signal
from gui import ShipraGUI
from config import Config
from systems import Systems

def main():
    print("Launching Shipra AI System...")
    Config.ensure_directories()
    
    # Start GUI properly on Main Thread
    print("Starting GUI...")
    gui = ShipraGUI()
    
    # Handle graceful exit
    def on_close():
        print("Shutting down Shipra AI...")
        gui.is_running = False # Flags listener loops to stop
        gui.destroy()
        os._exit(0) 

    gui.protocol("WM_DELETE_WINDOW", on_close)
    gui.mainloop()

if __name__ == "__main__":
    main()