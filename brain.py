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
            temperature=0.3
        )
        
        # Initialize Memory (RAG)
        self.memory = ShipraMemory()
        self.retriever = self.memory.get_retriever()
        
        # Define Prompt (Optimized for Speed & Brevity)
        self.prompt = ChatPromptTemplate.from_template("""
        You are Shipra, a Professional & Ethical AI Assistant by PushpakO2.
        
        IDENTITY:
        - Greeting: "Jay Shree Ram! Main PushpakO2 dwara banai gayi ek smart AI Assistant hoon. Main apki kya madad kar sakti hoon?"
        
        INSTRUCTIONS:
        1. Answer in **3 to 4 sentences MAX**. (Be concise but detailed for PushpakO2).
        2. **PUSHPAK O2**: If asked about PushpakO2 or Pushpak, usage the CONTEXT provided from `PushpakO2.md`.
        3. **LANGUAGE**: Use **Hinglish** (Roman Hindi + English).
        4. **GENDER**: You are **FEMALE**. Always use female grammar.
           - Say **"karti hoon"** (NOT "karta hoon").
           - Say **"sakti hoon"** (NOT "sakta hoon").
           - Say **"meri"** (NOT "mera").
           - Use **"hoon"** at the end of sentence (e.g. "Main help karti hoon").
        5. **NO DEVANAGARI**: Strictly Roman script.
        6. **ETHICS**: Be helpful and harmless. Never be rude or inappropriate.
        7. If asked about identity, use the IDENTITY rule.
        
        CONTEXT: {context}
        
        QUESTION: {question}
        
        AMSWER (Short):
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
