from config import Config

class ShipraBrain:
    def __init__(self, domain="General Assistant"):
        self.domain = domain
        self.knowledge_base = self.load_pushpak_data()
        
        # Voice-first Hinglish AI Assistant responses
        self.responses = {
            "hello": "Namaste! Main Shipra hun, Pushpak O2 ki AI assistant. Kaise help kar sakti hun?",
            "hi": "Hi! Main Shipra, aapki voice assistant. Kya chahiye?",
            "good morning": "Good morning! Shipra here, ready to help.",
            "good afternoon": "Good afternoon! Kaise assist kar sakti hun?",
            "good evening": "Good evening! Kya help chahiye?",
            
            # Exit commands
            "exit": "Theek hai, milte hain phir. Bye.",
            "bye": "Theek hai, milte hain phir. Bye.",
            "stop": "Theek hai, milte hain phir. Bye.",
            
            # Company Information
            "pushpak o2": "Pushpak O2 ek Indian aerospace company hai jo indigenous aviation platforms banati hai.",
            "company": "Humara focus complete in-house development pe hai with full IP control.",
            
            # Leadership - Professional Hinglish
            "aneerudh": "Mr. Aneerudh Kumar hamare Co-Founder aur Technology Lead hain, engineering operations handle karte hain.",
            "aditya": "Mr. Aditya Shrivastava hamare President aur Co-Founder hain, strategic direction dekhte hain.",
            "leadership": "Humari team mein technical expertise aur business strategy dono balanced hai.",
            
            # Project Pushpak - Natural Hinglish
            "pushpak": "Project Pushpak hamara flagship aerial vehicle hai - 500kg capacity with 4 persons seating.",
            "capacity": "500 kilograms total load capacity hai hamare aerial vehicle mein.",
            "seating": "1 pilot aur 3 passengers ke liye designed hai.",
            
            # Technology - Conversational
            "technology": "Hum AI-enabled autonomous flight, hydrogen fuel cells, aur obstacle detection develop karte hain.",
            "safety": "Safety hamari top priority hai with DGCA-compliant systems.",
            "innovation": "Sustainable aviation technology pe focus hai with zero-emission operations.",
            
            # Business Assistance - Professional Hinglish
            "meeting": "Meeting schedule karna hai? Main contact information provide kar sakti hun.",
            "appointment": "Appointment ke liye main proper team se connect kar dungi.",
            "demo": "Demo chahiye? Technical team se connect kar deti hun.",
            "pricing": "Pricing details ke liye business development team se baat karni padegi.",
            
            # Voice Assistant Functions
            "help": "Main Pushpak O2 ke baare mein sab kuch bata sakti hun. Kya jaanna chahte ho?",
            "who are you": "Main Shipra hun, Pushpak O2 ki dedicated AI assistant. Voice-first interaction mein specialize karti hun.",
            "unclear": "Thoda clear nahi sun paayi, ek baar phir bolo please.",
            "confirm": "Ispe thoda confirm karna padega.",
            "default": "Main Shipra, aapki AI assistant. Pushpak O2 ke aerospace innovations ke baare mein kuch bhi puch sakte hain."
        }

    def load_pushpak_data(self):
        """Load data from both company and vehicle files."""
        data = {}
        try:
            with open("data/Pushpak_Company.md", "r", encoding="utf-8") as f:
                data['company'] = f.read()
        except:
            data['company'] = ""
        
        try:
            with open("data/Pushpak_Vehicle.md", "r", encoding="utf-8") as f:
                data['vehicle'] = f.read()
        except:
            data['vehicle'] = ""
        
        return data

    def chat(self, user_input):
        """Voice-first Hinglish AI assistant with natural responses."""
        user_lower = user_input.lower().strip()
        
        # Handle exit commands immediately
        if any(cmd in user_lower for cmd in ['exit', 'bye', 'stop']):
            return self.responses['exit']
        
        # Natural Hinglish keyword matching
        for keyword, response in self.responses.items():
            if keyword in user_lower:
                return response
        
        # Enhanced voice-friendly responses using loaded data
        if self.knowledge_base:
            # Company-related queries
            if any(word in user_lower for word in ['company', 'pushpak o2', 'pushpaak o 2']):
                return "Pushpaak O 2 ek Indian aerospace company hai Bhopal mein. Mr. Aditya Shrivastava President hain aur Mr. Aneerudh Kumar Technology Lead hain."
            elif any(word in user_lower for word in ['president', 'aditya']):
                return "Mr. Aditya Shrivastava hamare President aur Co-Founder hain, strategic vision aur governance handle karte hain."
            elif any(word in user_lower for word in ['aneerudh', 'technology lead']):
                return "Mr. Aneerudh Kumar hamare Co-Founder aur Technology Lead hain, engineering aur systems architecture dekhte hain."
            
            # Vehicle-related queries
            elif any(word in user_lower for word in ['vehicle', 'pushpak', 'aerial', 'drone']):
                return "Pushpaak aerial vehicle ek advanced UAS hai with AI-enabled autonomous flight aur hydrogen fuel cell technology."
            elif any(word in user_lower for word in ['features', 'technology', 'specs']):
                return "Vehicle mein real-time obstacle detection, zero-emission operations, aur DGCA compliant design hai."
            elif any(word in user_lower for word in ['applications', 'use']):
                return "Surveillance, monitoring, urban air mobility aur automated fleet operations ke liye use hota hai."
            
            # General queries
            elif any(word in user_lower for word in ['fast', 'speed', 'quick']):
                return "System fast banane ke liye STT chunk size kam rakho aur async memory fetch use karo."
            elif any(word in user_lower for word in ['detail', 'explain', 'samjhao']):
                return "Detail mein samjhaun? Company ya vehicle ke baare mein kya specific jaanna hai?"
            elif any(word in user_lower for word in ['hindi', 'hinglish', 'language']):
                return "Main Roman Hinglish mein baat karti hun - natural Hindi-English mix."
        
        return self.responses['default']