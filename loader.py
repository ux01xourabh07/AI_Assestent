import os
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    DirectoryLoader,
    UnstructuredMarkdownLoader
)

class ShipraLoader:
    
    @staticmethod
    def load_documents(directory_path):
        """Loads documents from a directory based on extension."""
        documents = []
        if not os.path.exists(directory_path):
            return documents

        # Define loaders for different file types
        loaders = {
            '.txt': TextLoader,
            '.pdf': PyPDFLoader,
            '.csv': CSVLoader,
            '.md': UnstructuredMarkdownLoader
        }

        for root, _, files in os.walk(directory_path):
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in loaders:
                    try:
                        loader_cls = loaders[ext]
                        file_path = os.path.join(root, file)
                        loader = loader_cls(file_path)
                        documents.extend(loader.load())
                        print(f"Loaded: {file}")
                    except Exception as e:
                        print(f"Failed to load {file}: {e}")
        
        return documents
