import threading
import uvicorn
import time
import os
import signal
from gui import ShipraGUI
from config import Config
from systems import Systems

# Import the FastAPI app
try:
    from server import app as api_app
except ImportError:
    api_app = None

def run_server():
    """Runs the FastAPI server."""
    if api_app:
        print("Starting API Server on port 5000...")
        # log_level="error" suppresses the massive info logs to keep CLI clean for GUI
        uvicorn.run(api_app, host="127.0.0.1", port=5000, log_level="info")
    else:
        print("API Server module not found. Skipping.")

def main():
    print("Launching Shipra AI System...")
    Config.ensure_directories()
    
    # 1. Start Server in Background Thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Give server a moment to start (optional, just for visual CLI order)
    time.sleep(1)
    
    # 2. Start GUI properly on Main Thread
    print("Starting GUI...")
    gui = ShipraGUI()
    
    # Handle graceful exit
    def on_close():
        print("Shutting down Shipra AI...")
        gui.is_running = False # Flags listener loops to stop
        gui.destroy()
        # Daemon thread for server will die automatically when main thread exits
        os._exit(0) # Force kill to ensure uvicorn doesn't hang

    gui.protocol("WM_DELETE_WINDOW", on_close)
    gui.mainloop()

if __name__ == "__main__":
    main()