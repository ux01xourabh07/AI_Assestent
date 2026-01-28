from config import Config

class ShipraBrain:
    def __init__(self, domain="General Assistant"):
        self.domain = domain
        self.knowledge_base = self.load_pushpak_data()
        
        # Professional AI Assistant responses
        self.responses = {
            "hello": "Good day! I'm Shipra, your AI assistant from Pushpak O2. How may I assist you today?",
            "hi": "Hello! I'm Shipra, your professional AI assistant. What can I help you with?",
            "good morning": "Good morning! I'm Shipra, ready to assist you with any inquiries about Pushpak O2.",
            "good afternoon": "Good afternoon! How may I be of service to you today?",
            "good evening": "Good evening! I'm here to help with any questions you may have.",
            
            # Professional Company Responses
            "pushpak o2": "Pushpak O2 is a leading Indian aerospace company specializing in indigenous aviation platforms. We focus on complete in-house development with full IP control.",
            "company": "Our organization emphasizes cutting-edge aerospace engineering with complete control over design, manufacturing, and system integration.",
            "services": "We provide advanced aviation solutions including UAS, eVTOL systems, and autonomous flight technologies.",
            
            # Executive Information
            "aneerudh": "Mr. Aneerudh Kumar serves as our Co-Founder and Technology Lead, overseeing all engineering operations and system architecture.",
            "aditya": "Mr. Aditya Shrivastava is our President and Co-Founder, responsible for strategic direction and regulatory compliance.",
            "leadership": "Our leadership combines deep technical expertise with strategic business acumen to drive aerospace innovation.",
            "management": "Our executive team ensures balanced engineering innovation with regulatory compliance and business strategy.",
            
            # Professional Project Information
            "pushpak": "Project Pushpak represents our flagship aerial mobility solution - a 500kg capacity vehicle designed for urban transportation with seating for 4 persons.",
            "specifications": "Project Pushpak features a 500kg load capacity, accommodates 1 pilot and 3 passengers, with aerodynamically optimized design.",
            "capacity": "Our aerial vehicle maintains a total load capacity of 500 kilograms for optimal performance.",
            "seating": "The aircraft configuration includes one dedicated pilot position and three passenger seats for efficient urban transport.",
            
            # Technical Capabilities
            "technology": "We develop advanced systems including AI-enabled autonomous flight, hydrogen fuel cells, and real-time obstacle detection.",
            "innovation": "Our R&D focuses on sustainable aviation technology, eVTOL capabilities, and smart fleet management solutions.",
            "safety": "Safety remains our top priority with DGCA-compliant systems and stability-focused design principles.",
            "sustainability": "We utilize hydrogen fuel cell technology for zero-emission, environmentally responsible operations.",
            
            # Business Inquiries
            "meeting": "I can help coordinate information for meetings. Please specify your requirements or contact preferences.",
            "appointment": "For scheduling appointments with our executives, I can provide the necessary contact information and availability.",
            "contact": "I can assist with connecting you to the appropriate department or executive team member.",
            "partnership": "For partnership opportunities, I can direct you to our business development team.",
            "investment": "Investment inquiries can be routed to our executive leadership for proper evaluation.",
            
            # Professional Assistance
            "help": "I'm here to provide comprehensive information about Pushpak O2's capabilities, projects, and services. What specific area interests you?",
            "information": "I can provide detailed information about our aerospace technologies, leadership team, or current projects. What would you like to know?",
            "who are you": "I'm Shipra, your dedicated AI assistant representing Pushpak O2. I'm here to provide professional support and information.",
            "default": "I'm Shipra, your professional AI assistant from Pushpak O2. I'm here to help with any inquiries about our aerospace innovations, leadership, or services. How may I assist you?"
        }

    def load_pushpak_data(self):
        """Load data from PushpakO2.md file."""
        try:
            with open("data/PushpakO2.md", "r", encoding="utf-8") as f:
                return f.read()
        except:
            return ""

    def chat(self, user_input):
        """Professional AI assistant response system."""
        user_lower = user_input.lower()
        
        # Professional greeting detection
        greetings = ['good morning', 'good afternoon', 'good evening']
        for greeting in greetings:
            if greeting in user_lower:
                return self.responses[greeting]
        
        # Professional keyword matching
        for keyword, response in self.responses.items():
            if keyword in user_lower:
                return response
        
        # Enhanced professional responses
        if self.knowledge_base:
            if any(word in user_lower for word in ['schedule', 'calendar', 'time']):
                return "I can assist with scheduling information. Please let me know your specific requirements or preferred contact method."
            elif any(word in user_lower for word in ['demo', 'presentation', 'showcase']):
                return "For product demonstrations or presentations, I can connect you with our technical team. What specific aspects interest you?"
            elif any(word in user_lower for word in ['quote', 'pricing', 'cost']):
                return "For pricing information and quotes, I'll direct you to our business development team who can provide detailed proposals."
            elif any(word in user_lower for word in ['technical', 'specification', 'details']):
                return "I can provide comprehensive technical specifications. Our Project Pushpak features advanced aerodynamic design with 500kg capacity."
        
        return self.responses["default"]
