
import os
from pymongo import MongoClient, TEXT
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import Config

class MongoKeywordRetriever:
    """
    A Keyword/Text-Search based retriever using Local MongoDB.
    """
    def __init__(self, collection, k=4):
        self.collection = collection
        self.k = k

    def invoke(self, query: str):
        """
        Retrieves documents using MongoDB Text Search.
        """
        if self.collection is None:
            return []

        # MongoDB Text Search
        # Results are sorted by relevance score
        cursor = self.collection.find(
            {"$text": {"$search": query}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(self.k)
        
        docs = []
        for doc in cursor:
            docs.append(Document(
                page_content=doc.get("page_content", ""),
                metadata=doc.get("metadata", {})
            ))
            
        # Fallback: If text search returns nothing (e.g., stop words or no match), 
        # try a simple regex for critical entities?
        # For now, we trust the text index.
        
        return docs

class ShipraMemory:
    def __init__(self):
        # Connect to Local MongoDB
        try:
            # Default local connection
            self.client = MongoClient("mongodb://localhost:27017/")
            self.db = self.client["shipra_db"]
            self.collection = self.db["knowledge"]
            print("[Memory] Connected to MongoDB (Local).")
            
            # Ensure Text Index exists for search
            self.collection.create_index([("page_content", TEXT)])
            
        except Exception as e:
            print(f"[Memory] MongoDB Connection Failed: {e}")
            self.collection = None

    def add_documents(self, documents):
        """Adds documents to MongoDB."""
        if not documents:
            return "No documents to add."
        
        if self.collection is None:
            return "MongoDB connection failed. Cannot add documents."
            
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)
        
        data_to_insert = []
        for chunk in chunks:
            data_to_insert.append({
                "page_content": chunk.page_content,
                "metadata": chunk.metadata
            })
        
        if data_to_insert:
            # Clear old knowledge to keep training fresh (Simulates 'Training')
            self.collection.delete_many({}) 
            self.collection.insert_many(data_to_insert)
            
        return f"Added {len(chunks)} chunks to MongoDB."
        
    def similarity_search(self, query, k=4):
        """Legacy method if called directly."""
        retriever = self.get_retriever()
        return retriever.invoke(query)
        
    def get_retriever(self):
        """Returns the keyword retriever."""
        return MongoKeywordRetriever(self.collection)
