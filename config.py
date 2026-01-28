import os

class Config:
    # Fastest model options (uncomment to use)
    # MODEL_NAME = "phi3:mini"        # Ultra-fast 3.8B model
    # MODEL_NAME = "gemma2:2b"        # Fast 2B model  
    MODEL_NAME = "llama3.2:1b"       # Current fast model
    BASE_URL = "http://localhost:11434"

    # Persistence Paths
    CHROMA_PERSIST_DIRECTORY = os.path.join(os.getcwd(), "chroma_db")
    DOCUMENTS_DIRECTORY = os.path.join(os.getcwd(), "data")

    # Fast Embeddings Model
    EMBEDDING_MODEL_NAME = "nomic-embed-text"
    
    # Ultra-fast Performance Settings
    MAX_RESPONSE_LENGTH = 50
    CONTEXT_LIMIT = 1
    HISTORY_LIMIT = 0
    
    # Fastest model options (uncomment to use)
    # MODEL_NAME = "phi3:mini"        # Ultra-fast 3.8B model
    # MODEL_NAME = "gemma2:2b"        # Fast 2B model  
    MODEL_NAME = "llama3.2:1b"       # Current fast model
    
    @staticmethod
    def ensure_directories():
        os.makedirs(Config.CHROMA_PERSIST_DIRECTORY, exist_ok=True)
        os.makedirs(Config.DOCUMENTS_DIRECTORY, exist_ok=True)
