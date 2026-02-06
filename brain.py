from config import Config
import os
import re
import random

class ShipraBrain:
    def __init__(self, domain="General Assistant"):
        self.domain = domain
        self.company_data = self.load_company_data()
        self.vehicle_data = self.load_vehicle_data()
        self.response_counter = {}
        self.force_english = False  # Flag to force English responses
        
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
    
    def detect_language(self, text):
        """Detect if input is primarily Hindi or English"""
        # If force_english flag is set, always return english
        if self.force_english:
            return 'english'
        
        # Otherwise, always return hindi for Hinglish mode (default)
        # This ensures Hinglish responses unless explicitly set to English
        hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
        
        # If there are Hindi characters, definitely Hindi
        if hindi_chars > 0:
            return 'hindi'
        
        # For English input without force_english flag, use Hinglish (hindi mode)
        return 'hindi'
    
    def get_varied_response(self, key, responses):
        """Get varied response to avoid repetition"""
        if key not in self.response_counter:
            self.response_counter[key] = 0
        
        response = responses[self.response_counter[key] % len(responses)]
        self.response_counter[key] += 1
        return response
    
    def get_unknown_response(self, lang):
        """Return unknown response based on language"""
        if lang == 'hindi':
            responses = [
                "मुझे इस बारे में जानकारी नहीं है।",
                "यह मेरी जानकारी में नहीं है।",
                "इसके बारे में मुझे पता नहीं है।"
            ]
        else:
            responses = [
                "I don't have knowledge about this.",
                "This is not in my knowledge base.",
                "I'm not aware of this information."
            ]
        return self.get_varied_response('unknown', responses)
    
    def analyze_query(self, user_input):
        """Analyze user query and return relevant information"""
        query = user_input.lower().strip()
        
        # Check for language preference requests
        if any(phrase in query for phrase in ['speak in english', 'speak english', 'english please', 'i cannot understand', 'i dont understand', 'english mein bolo', 'english me bolo']):
            self.force_english = True
            return "Sure! I will speak in English from now on. How can I help you?"
        
        # Check for Hindi preference requests
        if any(phrase in query for phrase in ['speak in hindi', 'hindi mein bolo', 'hindi please', 'should i talk in hindi', 'can i speak hindi', 'hindi me baat karu', 'hindi mai baat karo', 'hindi bolo', 'hindi me bolo', 'talk in hindi', 'speak hindi']):
            self.force_english = False
            return "Theek hai! Main ab Hindi mein baat karungi. Kaise madad kar sakti hun?"
        
        lang = self.detect_language(user_input)
        
        # Company-related queries
        if any(word in query for word in ['company', 'pushpak o2', 'pushpak auto', 'leadership', 'president', 'aditya', 'aneerudh', 'location', 'bhopal', 'mission', 'founder', 'co-founder', 'kaun hai', 'who is']):
            return self.get_company_info(query, lang)
        
        # Vehicle-related queries  
        elif any(word in query for word in ['vehicle', 'pushpak', 'aerial', 'drone', 'uas', 'features', 'technology', 'hydrogen', 'autonomous', 'capacity', 'load']):
            return self.get_vehicle_info(query, lang)
        
        # Personal questions about Shipra
        elif any(word in query for word in ['who are you', 'kaun ho', 'tum kaun', 'your purpose', 'tumhara purpose', 'why you', 'kyu banaya']):
            if 'purpose' in query or 'kyu' in query:
                if lang == 'hindi':
                    responses = [
                        "मेरा purpose है Pushpak vehicle के बारे में जानकारी देना। मैं aerial vehicle की features, capacity और technology के बारे में बता सकती हूं।",
                        "मुझे इसलिए बनाया गया है ताकि मैं Pushpak vehicle की information provide कर सकूं। मैं vehicle specifications और capabilities के बारे में बताती हूं।",
                        "मेरा काम है Pushpak aerial vehicle के बारे में बताना - उसकी capacity, features और technology।"
                    ]
                else:
                    responses = [
                        "My purpose is to provide information about the Pushpak vehicle. I can tell you about the aerial vehicle's features, capacity, and technology.",
                        "I was created to provide information about the Pushpak vehicle. I share details about vehicle specifications and capabilities.",
                        "My job is to inform about the Pushpak aerial vehicle - its capacity, features, and technology."
                    ]
            else:
                if lang == 'hindi':
                    responses = [
                        "मैं शिप्रा हूं, Pushpak vehicle की AI assistant। मैं aerial vehicle के बारे में जानकारी देती हूं।",
                        "नमस्ते! मैं Shipra, Pushpak vehicle की voice assistant। मैं vehicle information के लिए यहां हूं।",
                        "मैं शिप्रा, Pushpak aerial vehicle की dedicated assistant हूं। मैं vehicle technology के बारे में बता सकती हूं।"
                    ]
                else:
                    responses = [
                        "I am Shipra, the AI assistant for Pushpak vehicle. I provide information about the aerial vehicle.",
                        "Hello! I'm Shipra, the voice assistant for Pushpak vehicle. I'm here to help with vehicle information.",
                        "I am Shipra, the dedicated assistant for Pushpak aerial vehicle. I can tell you about vehicle technology."
                    ]
            return self.get_varied_response('identity', responses)
        
        # General greetings and social responses
        elif any(word in query for word in ['hello', 'hi', 'hey', 'namaste', 'नमस्ते', 'good morning', 'good afternoon', 'good evening', 'thank you', 'thanks', 'dhanyawad', 'धन्यवाद']):
            if 'thank' in query or 'dhanyawad' in query or 'धन्यवाद' in query:
                if lang == 'hindi':
                    responses = [
                        "कोई बात नहीं! खुशी से मदद की।",
                        "स्वागत है! और कुछ चाहिए?",
                        "धन्यवाद आपका! कुछ और पूछना है?"
                    ]
                else:
                    responses = [
                        "No problem! Happy to help.",
                        "You're welcome! Anything else?",
                        "Thank you! Any other questions?"
                    ]
            elif 'good morning' in query:
                if lang == 'hindi':
                    responses = [
                        "सुप्रभात! आज कैसे मदद कर सकती हूं?",
                        "गुड मॉर्निंग! दिन शुभ हो, क्या चाहिए?",
                        "नमस्कार! सुबह की शुरुआत कैसे करें?"
                    ]
                else:
                    responses = [
                        "Good morning! How can I help you today?",
                        "Good morning! Have a great day, what do you need?",
                        "Hello! How shall we start the morning?"
                    ]
            elif 'good afternoon' in query:
                if lang == 'hindi':
                    responses = [
                        "नमस्कार! दोपहर कैसी जा रही है?",
                        "गुड आफ्टरनून! कैसे सहायता करूं?",
                        "प्रणाम! दिन कैसा चल रहा है?"
                    ]
                else:
                    responses = [
                        "Hello! How is your afternoon going?",
                        "Good afternoon! How can I assist you?",
                        "Greetings! How is your day going?"
                    ]
            elif 'good evening' in query:
                if lang == 'hindi':
                    responses = [
                        "शुभ संध्या! शाम कैसी है?",
                        "गुड इवनिंग! कैसे मदद करूं?",
                        "नमस्कार! संध्या की शुरुआत अच्छी हो!"
                    ]
                else:
                    responses = [
                        "Good evening! How is your evening?",
                        "Good evening! How can I help?",
                        "Hello! Have a great evening!"
                    ]
            else:
                if lang == 'hindi':
                    responses = [
                        "नमस्ते! मैं शिप्रा हूं, Pushpak O2 की AI असिस्टेंट। कैसे मदद कर सकती हूं?",
                        "हैलो! शिप्रा यहां, आपकी सेवा में। क्या चाहिए?",
                        "नमस्कार! मैं Pushpak O2 की AI असिस्टेंट शिप्रा। बताइए कैसे सहायता करूं?"
                    ]
                else:
                    responses = [
                        "Hello! I am Shipra, the AI assistant for Pushpak O2. How can I help you?",
                        "Hi! Shipra here, at your service. What do you need?",
                        "Greetings! I am Shipra, the AI assistant for Pushpak O2. How can I assist you?"
                    ]
            return self.get_varied_response('greeting', responses)
        
        # Exit commands
        elif any(word in query for word in ['bye', 'goodbye', 'exit', 'stop', 'alvida', 'अलविदा', 'tata', 'see you']):
            if lang == 'hindi':
                responses = [
                    "धन्यवाद! फिर मिलते हैं।",
                    "अच्छा, फिर बात करते हैं। नमस्ते!",
                    "ठीक है, अलविदा! खुश रहिए।"
                ]
            else:
                responses = [
                    "Thank you! See you again.",
                    "Alright, talk to you later. Goodbye!",
                    "Okay, goodbye! Stay happy."
                ]
            return self.get_varied_response('goodbye', responses)
        
        else:
            return self.get_unknown_response(lang)
    
    def get_company_info(self, query, lang):
        """Extract specific company information based on query"""
        # Override lang if force_english is True
        if self.force_english:
            lang = 'english'
            
        if 'president' in query or 'aditya' in query:
            if lang == 'hindi':
                responses = [
                    "श्री आदित्य श्रीवास्तव हमारे President और Co-Founder हैं। वे strategic vision और governance handle करते हैं।",
                    "आदित्य जी Pushpak O2 के President हैं। Company की strategic direction वे देखते हैं।",
                    "Mr. Aditya Shrivastava हमारे मुख्य नेता हैं, President के रूप में governance का काम करते हैं।"
                ]
            else:
                responses = [
                    "Mr. Aditya Shrivastava is our President and Co-Founder. He handles strategic vision and governance.",
                    "Aditya ji is the President of Pushpak O2. He oversees the company's strategic direction.",
                    "Mr. Aditya Shrivastava is our chief leader, working as President handling governance."
                ]
            return self.get_varied_response('president', responses)
            
        elif 'aneerudh' in query or 'technology lead' in query:
            if lang == 'hindi':
                responses = [
                    "श्री अनीरुध कुमार हमारे Co-Founder और Technology Lead हैं। वे engineering और systems architecture देखते हैं।",
                    "अनीरुध जी technical operations handle करते हैं। वे हमारे Technology Lead हैं।",
                    "Mr. Aneerudh Kumar engineering का पूरा काम देखते हैं, Co-Founder भी हैं।"
                ]
            else:
                responses = [
                    "Mr. Aneerudh Kumar is our Co-Founder and Technology Lead. He handles engineering and systems architecture.",
                    "Aneerudh ji handles technical operations. He is our Technology Lead.",
                    "Mr. Aneerudh Kumar oversees all engineering work and is also a Co-Founder."
                ]
            return self.get_varied_response('aneerudh', responses)
            
        elif ('founder' in query and ('kaun hai' in query or 'who is' in query)) or ('pushpak auto' in query and ('founder' in query or 'kaun hai' in query)):
            if lang == 'hindi':
                responses = [
                    "Pushpak O2 के दो co-founders हैं - Mr. Aditya Shrivastava जो President हैं और Mr. Aneerudh Kumar जो Technology Lead हैं। दोनों मिलकर company को चला रहे हैं।",
                    "Pushpak auto यानी Pushpak O2 के founders हैं Aditya Shrivastava साहब (President) और Aneerudh Kumar जी (Technology Lead)। दोनों co-founders हैं।",
                    "हमारे company के दो मुख्य नेता हैं - Aditya ji जो business operations handle करते हैं और Aneerudh ji जो technical work देखते हैं।"
                ]
            else:
                responses = [
                    "Pushpak O2 has two co-founders - Mr. Aditya Shrivastava who is the President and Mr. Aneerudh Kumar who is the Technology Lead. Both are running the company together.",
                    "Pushpak auto, which is Pushpak O2, has founders Aditya Shrivastava (President) and Aneerudh Kumar (Technology Lead). Both are co-founders.",
                    "Our company has two main leaders - Aditya ji who handles business operations and Aneerudh ji who oversees technical work."
                ]
            return self.get_varied_response('pushpak_auto_founders', responses)
        elif 'founder' in query or 'co-founder' in query:
            if lang == 'hindi':
                responses = [
                    "Pushpak O2 के दो co-founders हैं - Mr. Aditya Shrivastava (President) और Mr. Aneerudh Kumar (Technology Lead)। दोनों मिलकर company को आगे बढ़ा रहे हैं।",
                    "हमारे founders हैं Aditya ji जो business operations handle करते हैं और Aneerudh ji जो technical side देखते हैं।",
                    "Company के दो मुख्य नेता हैं - strategic leadership के लिए Aditya Shrivastava और technical innovation के लिए Aneerudh Kumar।"
                ]
            else:
                responses = [
                    "Pushpak O2 has two co-founders - Mr. Aditya Shrivastava (President) and Mr. Aneerudh Kumar (Technology Lead). Both are advancing the company together.",
                    "Our founders are Aditya ji who handles business operations and Aneerudh ji who oversees the technical side.",
                    "The company has two main leaders - Aditya Shrivastava for strategic leadership and Aneerudh Kumar for technical innovation."
                ]
        elif 'location' in query or 'bhopal' in query:
            if lang == 'hindi':
                responses = [
                    "Pushpak O2 का headquarters भोपाल, मध्य प्रदेश में है।",
                    "हमारा मुख्यालय भोपाल में स्थित है, MP में।",
                    "Company का base भोपाल, मध्य प्रदेश में है।"
                ]
            else:
                responses = [
                    "Pushpak O2's headquarters is in Bhopal, Madhya Pradesh.",
                    "Our headquarters is located in Bhopal, MP.",
                    "The company's base is in Bhopal, Madhya Pradesh."
                ]
            return self.get_varied_response('location', responses)
            
        else:
            if lang == 'hindi':
                responses = [
                    "Pushpak O2 एक Indian aerospace company है जो indigenous aviation platforms और unmanned aerial systems develop करती है।",
                    "यह भारतीय एयरोस्पेस कंपनी है जो स्वदेशी विमानन तकनीक बनाती है।",
                    "हमारी कंपनी indigenous aircraft और drone technology में काम करती है।"
                ]
            else:
                responses = [
                    "Pushpak O2 is an Indian aerospace company that develops indigenous aviation platforms and unmanned aerial systems.",
                    "It is an Indian aerospace company that builds indigenous aviation technology.",
                    "Our company works in indigenous aircraft and drone technology."
                ]
            return self.get_varied_response('company_general', responses)
    
    def get_vehicle_info(self, query, lang):
        """Extract specific vehicle information based on query"""
        # Override lang if force_english is True
        if self.force_english:
            lang = 'english'
            
        if 'capacity' in query or 'load' in query or 'person' in query:
            if lang == 'hindi':
                responses = [
                    "Pushpak vehicle की load capacity 500kg है या 4 persons तक ले जा सकता है।",
                    "यह 4 लोगों को carry कर सकता है या 500 किलो वजन उठा सकता है।",
                    "इसमें 4 व्यक्ति बैठ सकते हैं या 500kg का भार ले जा सकता है।"
                ]
            else:
                responses = [
                    "Pushpak vehicle has a load capacity of 500kg or can carry up to 4 persons.",
                    "It can carry 4 people or lift 500 kilograms of weight.",
                    "The vehicle can seat 4 persons or carry a load of 500kg."
                ]
            return self.get_varied_response('capacity', responses)
            
        elif 'features' in query:
            if lang == 'hindi':
                responses = [
                    "Pushpak vehicle में AI-enabled autonomous flight, real-time obstacle detection, hydrogen fuel cell power, और zero-emission operations है।",
                    "इसमें स्वचालित उड़ान, बाधा पहचान, हाइड्रोजन ईंधन और शून्य प्रदूषण की सुविधा है।",
                    "Vehicle में AI flight control, obstacle avoidance, hydrogen power और eco-friendly operations हैं।"
                ]
            else:
                responses = [
                    "Pushpak vehicle has AI-enabled autonomous flight, real-time obstacle detection, hydrogen fuel cell power, and zero-emission operations.",
                    "It features autonomous flight, obstacle detection, hydrogen fuel, and pollution-free operations.",
                    "The vehicle has AI flight control, obstacle avoidance, hydrogen power, and eco-friendly operations."
                ]
            return self.get_varied_response('features', responses)
            
        else:
            if lang == 'hindi':
                responses = [
                    "Pushpak एक advanced unmanned aerial system है with hybrid capabilities और DGCA compliant design।",
                    "यह एक उन्नत ड्रोन है जो hybrid technology और DGCA मानकों के अनुसार बना है।",
                    "Pushpak aerial vehicle एक स्मार्ट UAS है जो सभी aviation नियमों का पालन करता है।"
                ]
            else:
                responses = [
                    "Pushpak is an advanced unmanned aerial system with hybrid capabilities and DGCA compliant design.",
                    "It is an advanced drone built with hybrid technology and DGCA standards.",
                    "Pushpak aerial vehicle is a smart UAS that complies with all aviation regulations."
                ]
            return self.get_varied_response('vehicle_general', responses)
    
    def chat(self, user_input):
        """Main chat function that analyzes and responds"""
        return self.analyze_query(user_input)