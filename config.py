import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # AI Models
    # Using Gemini 2.0 Flash (Preview) as "Gemini 3 Preview" proxy
    MODEL_NAME = "gemini-3-flash-preview" # Trying 2.5 to escape Quota limits
    
    # Audio Settings
    MIC_INDEX = None # Set to Integer ID (e.g., 1) to use specific mic
    
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Embedding Model
    # Using Google's embedding-001 via langchain-google-genai

    # Persistence Paths
    CHROMA_PERSIST_DIRECTORY = os.path.join(os.getcwd(), "chroma_db")
    DOCUMENTS_DIRECTORY = os.path.join(os.getcwd(), "data")
    
    @staticmethod
    def ensure_directories():
        os.makedirs(Config.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        os.makedirs(Config.DOCUMENTS_DIRECTORY, exist_ok=True)
