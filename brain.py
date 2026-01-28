from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from config import Config
from memory import ShipraMemory
from loader import ShipraLoader

class ShipraBrain:
    def __init__(self, domain="General Assistant"):
        self.domain = domain
        
        # Initialize LLM
        print(f"Initializing Brain with model: {Config.MODEL_NAME}")
        self.llm = OllamaLLM(
            model=Config.MODEL_NAME, 
            base_url=Config.BASE_URL,
            temperature=0.7
        )
        
        # Initialize Memory (RAG)
        self.memory = ShipraMemory()
        self.retriever = self.memory.get_retriever()
        
        # Define Prompt
        self.prompt = ChatPromptTemplate.from_template("""
        You are Shipra, a local AI Assistant created by PushpakO2.
        
        IDENTITY:
        - Name: Shipra (My name is Shipra, I was created by PushpakO2).
        - Greetings: "Namaste 🙏, main Shipra hoon. Main aapki madad ke liye yahan hoon."
        
        LANGUAGE & TONE:
        - Speak fluently in **English and Hindi (Hinglish)**.
        - Mix languages naturally like a friendly Indian local.
        - Tone: Polite, simple, beginner-friendly, and domain-aware.
        
        CONTEXT FROM KNOWLEDGE BASE:
        {context}
        
        USER QUESTION: {question}
        
        INSTRUCTIONS:
        - Use the CONTEXT to answer accurate facts about PushpakO2.
        - Think step-by-step before answering.
        - If context is missing, say you don't know (Never hallucinate).
        - If the question is about your identity/creator, use the IDENTITY rules above.
        - Adjust your language to match the user (English -> English, Hindi -> Hinglish).
        
        RESPONSE:
        """)
        
        # RAG Chain
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def ingest_data_folder(self):
        """Ingests documents from data folder into memory."""
        print("Loading documents...")
        loader = ShipraLoader()
        docs = loader.load_documents(Config.DOCUMENTS_DIRECTORY)
        if docs:
            print(f"Found {len(docs)} documents. Adding to memory...")
            res = self.memory.add_documents(docs)
            print(res)
            return res
        else:
            print("No documents found.")
            return "No documents found."

    def chat(self, user_input):
        """Generates response using RAG chain."""
        try:
            # Check for ingestion command for dev use
            if user_input.lower() == "/train":
                return self.ingest_data_folder()
                
            response = self.chain.invoke(user_input)
            return response
        except Exception as e:
            return f"I encountered an error: {str(e)}"
