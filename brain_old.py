import json
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.runnables import RunnablePassthrough
from config import Config
from prompts import COGNITIVE_SYSTEM_PROMPT, SPEAKING_SYSTEM_PROMPT, FALLBACK_SYSTEM_PROMPT
from memory import ShipraMemory
from loader import ShipraLoader


# --- CLASSES ---

class CognitiveEngine:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_template(COGNITIVE_SYSTEM_PROMPT + "\n\nUSER INPUT: {question}\n\nCONTEXT SUMMARY: {context_summary}")
        self.chain = self.prompt | self.llm | JsonOutputParser()

    def think(self, question, context):
        """Analyzes input and returns a strategy dict."""
        print("Cognitive Engine: Thinking...")
        try:
            return self.chain.invoke({"question": question, "context_summary": context})
        except Exception as e:
            print(f"Cognitive Engine Error: {e}")
            return {
                "intent": "Unclear",
                "confidence_level": "low", # Default to low on error to trigger fallback
                "tone": "neutral",
                "language_style": ["Indian Hinglish, English"],
                "response_length": "short",
                "structure": "paragraph",
                "technical_depth": "intermediate",
                "examples_required": "no",
                "step_by_step": "no",
                "key_points": ["Directly answer the question based on context."],
                "warnings": [],
                "follow_up_suggestion": ""
            }

class SpeakingEngine:
    def __init__(self, llm):
        self.llm = llm
        # Standard Persona
        self.prompt = ChatPromptTemplate.from_template(SPEAKING_SYSTEM_PROMPT)
        self.chain = self.prompt | self.llm | StrOutputParser()
        
        # Fallback Persona (Uncertain/Noisy)
        self.fallback_prompt = ChatPromptTemplate.from_template(FALLBACK_SYSTEM_PROMPT)
        self.fallback_chain = self.fallback_prompt | self.llm | StrOutputParser()

    def speak(self, question, context, strategy):
        """Generates final response based on strategy."""
        
        # Check for Low Confidence -> Fallback Mode
        confidence = strategy.get("confidence_level", "medium").lower()
        if confidence == "low":
            print(f"Speaking Engine: Activating Fallback Mode (Confidence: {confidence})...")
            return self.fallback_chain.invoke({
                "question": question,
                "strategy": json.dumps(strategy, indent=2)
            })

        # Normal Mode
        print(f"Speaking Engine: Generating response ({strategy.get('intent', 'Unknown')})...")
        language_style = strategy.get("language_style", "Roman Hinglish")
        return self.chain.invoke({
            "question": question,
            "context": context,
            "strategy": json.dumps(strategy, indent=2),
            "language_style": language_style
        })

class ShipraBrain:
    def __init__(self, domain="General Assistant"):
        self.domain = domain
        
        # Initialize LLM (model from config)
        print(f"Initializing Brain with model: {Config.MODEL_NAME}")
        
        if not Config.GOOGLE_API_KEY or os.getenv("GOOGLE_API_KEY") in Config.GOOGLE_API_KEY:
            print("CRITICAL WARNING: GOOGLE_API_KEY is missing in config.py or env variables.")
        
        self.llm = ChatGoogleGenerativeAI(
            model=Config.MODEL_NAME,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.1,
            convert_system_message_to_human=True # Sometimes needed for older chains, but safe here
        )
        
        # Initialize Components
        self.memory = ShipraMemory()
        self.retriever = self.memory.get_retriever()
        
        self.cognitive_engine = CognitiveEngine(self.llm)
        self.speaking_engine = SpeakingEngine(self.llm)

    def ingest_data_folder(self):
        """Ingests documents from data folder into memory."""
        print("Loading documents...")
        loader = ShipraLoader()
        docs = loader.load_documents(Config.DOCUMENTS_DIRECTORY)
        if docs:
            print(f"Found {len(docs)} documents. Adding to memory...")
            res = self.memory.add_documents(docs)
            return res
        return "No documents found."

    def chat(self, user_input):
        """Orchestrates the 2-step cognitive pipeline."""
        try:
            # 1. Dev Command
            if user_input.strip().lower() == "/train":
                return self.ingest_data_folder()
                
            # 2. Retrieve Context (RAG)
            try:
                context_docs = self.retriever.invoke(user_input)
                context_text = "\n\n".join([doc.page_content for doc in context_docs]) if context_docs else "No specific context found."
            except Exception as e:
                print(f"RAG Error (Quota/Connection): {e}")
                context_text = "No specific context found (Retrieval Failed)."

            # --- MANUAL CONTEXT INJECTION (FALLBACK) ---
            # If RAG fails or keywords match specific entities, force inject the file content.
            # This ensures "Pushpak" is known even if API quota is dead.
            input_lower = user_input.lower()
            
            # 1. Pushpak (Vehicle)
            if "pushpak" in input_lower and "company" not in input_lower and "o 2" not in input_lower:
                try:
                    with open(os.path.join(Config.DOCUMENTS_DIRECTORY, "Pushpak_Vehicle.md"), "r", encoding="utf-8") as f:
                        vehicle_data = f.read()
                        context_text += "\n\n[MANUAL INJECTION: Pushpak_Vehicle.md]\n" + vehicle_data
                except Exception as ex:
                    print(f"Manual Injection Error (Vehicle): {ex}")

            # 2. Pushpak O 2 (Company)
            if "pushpak o 2" in input_lower or "company" in input_lower:
                 try:
                    with open(os.path.join(Config.DOCUMENTS_DIRECTORY, "Pushpak_Company.md"), "r", encoding="utf-8") as f:
                        company_data = f.read()
                        context_text += "\n\n[MANUAL INJECTION: Pushpak_Company.md]\n" + company_data
                 except Exception as ex:
                    print(f"Manual Injection Error (Company): {ex}")
            # -------------------------------------------

            # 3. Step 1: Cognitive Layer (Think)
            strategy = self.cognitive_engine.think(user_input, context_text)
            
            # 4. Step 2: Speaking Layer (Act)
            response = self.speaking_engine.speak(user_input, context_text, strategy)
            
            return response

        except Exception as e:
            error_msg = str(e).lower()
            print(f"Brain Error: {error_msg}")
            if "connection" in error_msg:
                return "Server connection failed. Please check your internet connection."
            return "Mujhe process karne mein kuch dikkat aa rahi hai."

