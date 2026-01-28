from systems import Systems
from config import Config
import os

def train():
    print("------------------------------------------------")
    print("   Shipra AI - Knowledge Base Training Tool     ")
    print("------------------------------------------------")
    
    # Ensure dirs
    Config.ensure_directories()
    
    # Check data
    if not os.path.exists(os.path.join(Config.DOCUMENTS_DIRECTORY, "PushpakO2.md")):
        print(f"WARNING: PushpakO2.md not found in {Config.DOCUMENTS_DIRECTORY}")
    
    # Initialize Brain (loads model & vector store)
    print("Initializing Brain...")
    brain = Systems.get_brain()
    
    # Ingest
    print(f"Ingesting documents from: {Config.DOCUMENTS_DIRECTORY}")
    result = brain.ingest_data_folder()
    
    print("------------------------------------------------")
    print(f"Training Result: {result}")
    print("------------------------------------------------")

if __name__ == "__main__":
    train()
