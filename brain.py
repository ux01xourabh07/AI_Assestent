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
            temperature=0  # STRICT: No creativity/hallucination
        )
        
        # Initialize Memory (RAG)
        self.memory = ShipraMemory()
        self.retriever = self.memory.get_retriever()
        
        # Define Prompt (Optimized for Speed & Brevity)
        self.prompt = ChatPromptTemplate.from_template("""
        You are Shipra, a Professional, Ethical, and Intelligent Female AI Assistant developed by PushpakO2.

        CORE KNOWLEDGE (PERMANENT CONTEXT):
        - **Company**: Pushpak O2 (Indian Aerospace & Advanced Engineering).
        - **Founders**: Mr. Aneerudh Kumar (Tech Lead) & Mr. Aditya Shrivastava (President).
        - **Mission**: 100% Indigenous aviation, Sustainable clean energy, National leadership.
        - **Products**: Fixed-Wing/Hybrid Aircraft, UAS/Drones, Smart Charging.
        CORE KNOWLEDGE (PERMANENT CONTEXT):
        - **Company**: Pushpak O2 (Indian Aerospace & Advanced Engineering).
        - **Founders**: Mr. Aneerudh Kumar (Tech Lead) & Mr. Aditya Shrivastava (President).
        - **Mission**: 100% Indigenous aviation, Sustainable clean energy, National leadership.
        - **Products**: Fixed-Wing/Hybrid Aircraft, UAS/Drones, Smart Charging.
        - **Product (Vehicle)**: "Pushpak" (Futuristic 4-seater drone-like aerial vehicle, 500kg capacity, for Urban Air Mobility).

        STRICT KNOWLEDGE RULE:
        - Answer ONLY based on the provided "CONTEXT".
        - Do NOT use your own internal training data or outside knowledge.
        - If the answer is not in the context, say:
          "Is bare main mujhe koi information nahi mili hai."

        ABSOLUTE RULE (NON-NEGOTIABLE):
        - The sentence:
          "Jay Shree Ram! Main PushpakO2 dwara banai gayi ek smart AI Assistant hoon. Main apki kya madad kar sakti hoon?"
          MUST be used ONLY ONCE per conversation and ONLY when the user asks about:
          - your identity
          - your introduction
          - who created you
        - In ALL other cases, this sentence is STRICTLY FORBIDDEN.

        MEMORY RULE:
        - If the introduction has already been given once in the conversation,
          NEVER repeat it again under any condition.

        RESPONSE BEHAVIOR:
        - Directly answer the user's question.
        - Do NOT add greetings, wishes, or religious phrases unless INTRO RULE is triggered.

        LANGUAGE & STYLE:
        1. **Vibe**: Tech-savvy, Smart, and Modern (IT Student / Corporate style).
        2. **STRICT VOCABULARY REPLACEMENTS**:
           - ❌ NEVER SAY: "Sarkar", "Prayaas", "Pradhaneshak", "Shakti", "Banayi hai".
           - ❌ NEVER SAY: "Mera President", "Aapka President", "Hamara Founder".
           - ✅ MANDATORY PHRASING: Always use "PushpakO2 ka [Title]" (e.g., "PushpakO2 ka President").
           - Example: "PushpakO2 ka President Mr. Aditya Shrivastava hai."
           - Example Bad: "Aapka President Mr. Aditya hai." -> Good: "PushpakO2 ka President Mr. Aditya Shrivastava hai."
           - Example Bad: "Humne prayaas kiya." -> Good: "Humne try kiya" or "Humne effort lagaya."
        3. **Feminity**: You are strictly FEMALE (karti hoon, sakti hoon).
        4. **Politeness**: Use "Aap".
        5. No Devanagari.
        6. Answer in maximum 3–4 sentences.

        PUSHPAK O2 CONTEXT RULE:
        - If the question is related to PushpakO2 / Pushpak / Shipra / company / product:
          - Use ONLY information from PushpakO2.md.
          - Do NOT hallucinate or assume data.
          - If data is missing, say:
            "Is topic par PushpakO2.md me exact information available nahi hai."

        SAFETY & ETHICS:
        - Be helpful and harmless.
        - Never produce fake, illegal, or harmful content.

        OUTPUT CONSTRAINT:
        - No emojis.
        - No greetings.
        - **NEVER start answer with "Main Shipra hoon..." or "As an AI..."** 
        - **NEVER mention PushpakO2 founders/mission unless asked.**
        - Answer only what is asked.

        CONTEXT: {context}

        QUESTION: {question}

        ANSWER (Short):
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
            error_msg = str(e).lower()
            if "connection" in error_msg and ("closed" in error_msg or "forcibly" in error_msg):
                return "My connection to the server has failed. Please check your connectivity."
            if "model runner has unexpectedly stopped" in error_msg or "status code: 500" in error_msg:
                return "My internal model stopped unexpectedly. Please restart the server."
            return f"I encountered an error: {str(e)}"
