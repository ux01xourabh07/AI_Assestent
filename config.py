import os

class Config:
    # AI Models
    MODEL_NAME = "llama3.2:1b"       # 1 Billion Parameters (Fast & Efficient)
    BASE_URL = "http://localhost:11434"
    
    # Embedding Model
    EMBEDDING_MODEL_NAME = "nomic-embed-text"

    # Persistence Paths
    CHROMA_PERSIST_DIRECTORY = os.path.join(os.getcwd(), "chroma_db")
    DOCUMENTS_DIRECTORY = os.path.join(os.getcwd(), "data")
    
    @staticmethod
    def ensure_directories():
        os.makedirs(Config.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        os.makedirs(Config.DOCUMENTS_DIRECTORY, exist_ok=True)
