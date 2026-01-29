import os
import glob
from langchain_community.document_loaders import (
    TextLoader,
    CSVLoader,
    PyPDFLoader
)
from langchain_core.documents import Document

class ShipraLoader:
    
    @staticmethod
    def load_documents(directory_path):
        """Loads documents from the data directory."""
        documents = []
        if not os.path.exists(directory_path):
            return documents
            
        # Recursive search for supported files
        for root, _, files in os.walk(directory_path):
            for file in files:
                full_path = os.path.join(root, file)
                try:
                    ext = os.path.splitext(file)[1].lower()
                    if ext == ".txt":
                        loader = TextLoader(full_path, encoding="utf-8")
                        documents.extend(loader.load())
                    elif ext == ".csv":
                        loader = CSVLoader(full_path, encoding="utf-8")
                        documents.extend(loader.load())
                    elif ext == ".md":
                        # Optimized: Read markdown as plain text to avoid 'unstructured' dependency
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        documents.append(Document(page_content=content, metadata={"source": full_path}))
                    elif ext == ".pdf":
                        loader = PyPDFLoader(full_path)
                        documents.extend(loader.load())
                    elif ext == ".json":
                        # Use simple JSON loader
                        import json
                        with open(full_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        content = json.dumps(data, indent=2)
                        documents.append(Document(page_content=content, metadata={"source": full_path}))
                except Exception as e:
                    print(f"Error loading {file}: {e}")
                    
        return documents
