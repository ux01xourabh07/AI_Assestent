import os
import chromadb
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import Config

class ShipraMemory:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model="nomic-embed-text",  # Standard efficient embedding model
            base_url=Config.BASE_URL
        )
        
        # Initialize Vector Store
        self.vector_store_path = Config.CHROMA_PERSIST_DIRECTORY
        self.vector_store = Chroma(
            persist_directory=self.vector_store_path,
            embedding_function=self.embeddings,
            collection_name="shipra_knowledge"
        )
        
    def add_documents(self, documents):
        """Adds documents to the vector store."""
        if not documents:
            return "No documents to add."
            
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        
        self.vector_store.add_documents(chunks)
        return f"Added {len(chunks)} chunks to memory."
        
    def similarity_search(self, query, k=4):
        """Searches for relevant documents."""
        return self.vector_store.similarity_search(query, k=k)
        
    def get_retriever(self):
        """Returns a retriever for LangChain chains."""
        return self.vector_store.as_retriever(search_kwargs={"k": 4})
