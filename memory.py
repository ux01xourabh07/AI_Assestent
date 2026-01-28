from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import Config
import os

class ShipraMemory:
    def __init__(self):
        self.embedding_function = OllamaEmbeddings(
            model=Config.MODEL_NAME, # Using the main model for embeddings to ensure availability
            base_url=Config.BASE_URL
        )
        
        self.vector_store = Chroma(
            persist_directory=Config.CHROMA_PERSIST_DIRECTORY,
            embedding_function=self.embedding_function,
            collection_name="shipra_knowledge_base"
        )
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    def add_documents(self, documents):
        """Splits and adds documents to the vector store."""
        if not documents:
            return "No documents to add."
        
        chunks = self.text_splitter.split_documents(documents)
        if chunks:
            self.vector_store.add_documents(chunks)
            # self.vector_store.persist() # Chroma 0.4+ persists automatically or via different methods, usually auto-persists in v0.5+
            return f"Added {len(chunks)} chunks from {len(documents)} documents to memory."
        return "No text chunks created."

    def query_memory(self, query, k=2):
        """Fast retrieval with embedding error handling."""
        try:
            results = self.vector_store.similarity_search(query, k=k)
            return results
        except Exception as e:
            if "dimension" in str(e).lower():
                print("Fixing embedding dimension mismatch...")
                self.fix_embedding_dimension_error()
                return []  # Return empty for this query
            print(f"Memory query error: {e}")
            return []
    
    def clear_memory(self):
        """Clear memory and recreate with correct embeddings."""
        try:
            self.vector_store.delete_collection()
        except: pass
        
        self.vector_store = Chroma(
            persist_directory=Config.CHROMA_PERSIST_DIRECTORY,
            embedding_function=self.embedding_function,
            collection_name="shipra_knowledge_base"
        )
        return "Memory cleared."
    
    def fix_embedding_dimension_error(self):
        """Fix embedding dimension mismatch by clearing and recreating."""
        import shutil
        try:
            shutil.rmtree(Config.CHROMA_PERSIST_DIRECTORY)
        except: pass
        
        Config.ensure_directories()
        self.__init__()
        return "Memory reset with correct embeddings."
