from config import Config
import os

class ShipraBrain:
    def __init__(self, domain="General Assistant"):
        self.domain = domain
        self.company_data = self.load_company_data()
        self.vehicle_data = self.load_vehicle_data()
        
    def load_company_data(self):
        """Load company information from Pushpak_Company.md"""
        try:
            with open("data/Pushpak_Company.md", "r", encoding="utf-8") as f:
                return f.read()
        except:
            return ""
    
    def load_vehicle_data(self):
        """Load vehicle information from Pushpak_Vehicle.md"""
        try:
            with open("data/Pushpak_Vehicle.md", "r", encoding="utf-8") as f:
                return f.read()
        except:
            return ""
    
    def analyze_query(self, user_input):
        """Analyze user query and return relevant information"""
        query = user_input.lower().strip()
        
        # Company-related queries
        if any(word in query for word in ['company', 'pushpaak o 2', 'pushpak o2', 'leadership', 'president', 'aditya', 'aneerudh', 'location', 'bhopal', 'mission']):
            return self.get_company_info(query)
        
        # Vehicle-related queries  
        elif any(word in query for word in ['vehicle', 'pushpaak', 'aerial', 'drone', 'uas', 'features', 'technology', 'hydrogen', 'autonomous']):
            return self.get_vehicle_info(query)
        
        # General greetings
        elif any(word in query for word in ['hello', 'hi', 'namaste']):
            return "Namaste! Main Shipra hun, Pushpaak O 2 ki AI assistant. Kaise help kar sakti hun?"
        
        # Exit commands
        elif any(word in query for word in ['bye', 'exit', 'stop']):
            return "Dhanyawad! Phir milte hain."
        
        else:
            return "Main Pushpaak O 2 aur hamare aerial vehicles ke baare mein bata sakti hun. Kya jaanna chahte hain?"
    
    def get_company_info(self, query):
        """Extract specific company information based on query"""
        if 'president' in query or 'aditya' in query:
            return "Mr. Aditya Shrivastava hamare President aur Co-Founder hain. Woh strategic vision aur governance handle karte hain."
        elif 'aneerudh' in query or 'technology lead' in query:
            return "Mr. Aneerudh Kumar hamare Co-Founder aur Technology Lead hain. Woh engineering aur systems architecture dekhte hain."
        elif 'location' in query or 'bhopal' in query:
            return "Pushpaak O 2 ka headquarters Bhopal, Madhya Pradesh mein hai."
        elif 'mission' in query:
            return "Hamara mission hai 100% indigenous aerospace innovation with DGCA compliance aur sustainable aviation solutions."
        else:
            return "Pushpaak O 2 ek Indian aerospace company hai jo indigenous aviation platforms aur unmanned aerial systems develop karti hai."
    
    def get_vehicle_info(self, query):
        """Extract specific vehicle information based on query"""
        if 'features' in query:
            return "Pushpaak vehicle mein AI-enabled autonomous flight, real-time obstacle detection, hydrogen fuel cell power, aur zero-emission operations hai."
        elif 'technology' in query:
            return "Vehicle mein hybrid fixed-wing design, autonomous navigation systems, sustainable energy solutions aur advanced flight control systems hai."
        elif 'applications' in query or 'use' in query:
            return "Surveillance aur monitoring, urban air mobility, automated fleet operations aur smart charging integration ke liye use hota hai."
        elif 'hydrogen' in query:
            return "Hamara vehicle hydrogen fuel cell technology use karta hai jo zero-emission operations provide karta hai."
        else:
            return "Pushpaak ek advanced unmanned aerial system hai with hybrid capabilities aur DGCA compliant design."
    
    def chat(self, user_input):
        """Main chat function that analyzes and responds"""
        return self.analyze_query(user_input)