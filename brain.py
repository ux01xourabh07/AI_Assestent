from config import Config
import os
import re
import random
from datetime import datetime
from weather import WeatherService

class ShipraBrain:
    def __init__(self, domain="General Assistant"):
        self.domain = domain
        self.company_data = self.load_company_data()
        self.vehicle_data = self.load_vehicle_data()
        self.response_counter = {}
        self.weather_service = WeatherService()
        
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
        # Check for explicit 'english' keyword in the query
        if 'english' in text.lower():
            return 'english'
        
        # Check for specific Hindi keywords that indicate Hinglish preference
        hinglish_indicators = ['bare', 'mein', 'batao', 'baare']
        if any(word in text.lower() for word in hinglish_indicators):
            return 'hindi'
        
        # Check for Hindi/Hinglish keywords
        hindi_keywords = ['hindi', 'hinglish', 'kaun', 'kya', 'kaise', 'kahan', 'kyun', 'kab', 
                         'hai', 'hain', 'hun', 'ho', 'ko', 'ka', 'ki', 'ke', 'se', 
                         'tak', 'par', 'aur', 'ya', 'bhi', 'tum', 'aap', 'main', 'yeh', 'veh']
        
        # Check for Devanagari characters
        hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
        if hindi_chars > 0:
            return 'hindi'
        
        # Count Hindi keywords in the text
        words = text.lower().split()
        hindi_word_count = sum(1 for word in words if word in hindi_keywords)
        
        # If more than 20% of words are Hindi keywords, use Hindi
        if len(words) > 0 and (hindi_word_count / len(words)) > 0.2:
            return 'hindi'
        
        # Default to English for pure English sentences
        return 'english'
    
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
                "Maaf kijiye, main sirf Pushpak O2 company aur vehicle ke baare mein jaankari de sakti hun. Iske baare mein mujhe pata nahi hai.",
                "Yeh meri expertise ke bahar hai. Main bas Pushpak O2 aur hamare aerial vehicle ke baare mein bata sakti hun.",
                "Main sirf Pushpak O2 ki assistant hun. Is topic ke baare mein mujhe jaankari nahi hai."
            ]
        else:
            responses = [
                "Sorry, I can only provide information about Pushpak O2 company and our vehicle. I don't have knowledge about this.",
                "This is outside my expertise. I can only tell you about Pushpak O2 and our aerial vehicle.",
                "I'm only an assistant for Pushpak O2. I don't have information about this topic."
            ]
        return self.get_varied_response('unknown', responses)
    
    def analyze_query(self, user_input):
        """Analyze user query and return relevant information"""
        query = user_input.lower().strip()
        
        # Language detection happens automatically per sentence now
        # No need for persistent language preference
        
        lang = self.detect_language(user_input)
        
        # Company-related queries
        if any(word in query for word in ['company', 'pushpak o2', 'pushpak auto', 'leadership', 'president', 'aditya', 'aneerudh', 'location', 'bhopal', 'mission', 'founder', 'co-founder', 'kaun hai', 'who is']):
            return self.get_company_info(query, lang)
        
        # Vehicle-related queries  
        elif any(word in query for word in ['vehicle', 'pushpak', 'aerial', 'drone', 'uas', 'features', 'technology', 'hydrogen', 'autonomous', 'capacity', 'load', 'speed', 'fast', 'kitni speed', 'speeed']):
            return self.get_vehicle_info(query, lang)
        
        # Weather queries
        elif any(word in query for word in ['weather', 'mausam', 'temperature', 'temp', 'garmi', 'sardi', 'baarish', 'rain', 'forecast', 'kal ka mausam', 'aaj ka mausam', 'waether', 'vedar']):
            return self.get_weather_info(query, lang)
        
        # How are you queries
        elif any(word in query for word in ['how are you', 'how r u', 'kaise ho', 'kaisi ho', 'kya haal', 'how do you do', 'how are u']):
            if lang == 'hindi':
                responses = [
                    "Main bilkul theek hun, dhanyawad! Aap kaise hain?",
                    "Main achhi hun, shukriya! Aap batao, kaise hain?",
                    "Sab badhiya hai! Aapka din kaisa ja raha hai?"
                ]
            else:
                responses = [
                    "I'm doing great, thank you! How are you?",
                    "I'm well, thanks for asking! How about you?",
                    "All good! How is your day going?"
                ]
            return self.get_varied_response('how_are_you', responses)
        
        # Time queries
        elif any(word in query for word in ['time', 'samay', 'kitne baje', 'what time', 'current time', 'abhi kitne baje']):
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            
            if lang == 'hindi':
                # Convert to 12-hour format for Hinglish
                period = "subah" if hour < 12 else "shaam" if hour < 18 else "raat"
                hour_12 = hour if hour <= 12 else hour - 12
                hour_12 = 12 if hour_12 == 0 else hour_12
                
                if minute == 0:
                    responses = [
                        f"Abhi {hour_12} baje {period} ke hain.",
                        f"Time hai {hour_12} baje {period}.",
                        f"{period} ke {hour_12} baj gaye hain."
                    ]
                else:
                    responses = [
                        f"Abhi {hour_12} baj kar {minute} minute {period} ke hain.",
                        f"Time hai {hour_12}:{minute:02d} {period}.",
                        f"{period} ke {hour_12} baj kar {minute} minute hue hain."
                    ]
            else:
                period = "AM" if hour < 12 else "PM"
                hour_12 = hour if hour <= 12 else hour - 12
                hour_12 = 12 if hour_12 == 0 else hour_12
                
                responses = [
                    f"It's {hour_12}:{minute:02d} {period}.",
                    f"The current time is {hour_12}:{minute:02d} {period}.",
                    f"Right now it's {hour_12}:{minute:02d} {period}."
                ]
            return self.get_varied_response('time', responses)
        
        # Personal questions about Shipra
        elif any(word in query for word in ['who are you', 'kaun ho', 'tum kaun', 'your purpose', 'tumhara purpose', 'why you', 'kyu banaya', 'apne bare', 'apne baare']):
            if 'purpose' in query or 'kyu' in query:
                if lang == 'hindi':
                    responses = [
                        "Mera purpose hai Pushpak vehicle ke baare mein jaankari dena. Main aerial vehicle ki features, capacity aur technology ke baare mein bata sakti hun.",
                        "Mujhe isliye banaya gaya hai taaki main Pushpak vehicle ki information provide kar sakun. Main vehicle specifications aur capabilities ke baare mein batati hun.",
                        "Mera kaam hai Pushpak aerial vehicle ke baare mein batana - uski capacity, features aur technology."
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
                        "Main Shipra hun, Pushpak vehicle ki AI assistant. Main aerial vehicle ke baare mein jaankari deti hun.",
                        "Namaste! Main Shipra, Pushpak vehicle ki voice assistant. Main vehicle information ke liye yahan hun.",
                        "Main Shipra, Pushpak aerial vehicle ki dedicated assistant hun. Main vehicle technology ke baare mein bata sakti hun."
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
                        "Koi baat nahi! Khushi se madad ki.",
                        "Swagat hai! Aur kuch chahiye?",
                        "Dhanyawad aapka! Kuch aur poochna hai?"
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
                        "Suprabhat! Aaj kaise madad kar sakti hun?",
                        "Good morning! Din shubh ho, kya chahiye?",
                        "Namaskar! Subah ki shuruaat kaise karein?"
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
                        "Namaskar! Dopahar kaisi ja rahi hai?",
                        "Good afternoon! Kaise sahayata karun?",
                        "Pranaam! Din kaisa chal raha hai?"
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
                        "Shubh sandhya! Shaam kaisi hai?",
                        "Good evening! Kaise madad karun?",
                        "Namaskar! Sandhya ki shuruaat achhi ho!"
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
                        "Namaste! Main Shipra hun, Pushpak O2 ki AI assistant. Kaise madad kar sakti hun?",
                        "Hello! Shipra yahan, aapki seva mein. Kya chahiye?",
                        "Namaskar! Main Pushpak O2 ki AI assistant Shipra. Bataiye kaise sahayata karun?"
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
            # Use Hinglish for Hindi exit words, English for English exit words
            if any(word in query for word in ['alvida', 'अलविदा', 'tata']):
                responses = [
                    "Dhanyawad! Phir milte hain. Jay Shree Ram.",
                    "Achha, phir baat karte hain. Namaste! Jay Shree Ram.",
                    "Theek hai, alvida! Khush rahiye. Jay Shree Ram."
                ]
            else:
                responses = [
                    "Thank you! See you again. Jay Shree Ram.",
                    "Alright, talk to you later. Goodbye! Jay Shree Ram.",
                    "Okay, goodbye! Stay happy. Jay Shree Ram."
                ]
            return self.get_varied_response('goodbye', responses)
        
        else:
            return self.get_unknown_response(lang)
    
    def get_company_info(self, query, lang):
        """Extract specific company information based on query"""
        # Language is already detected, no need to override
            
        if 'president' in query or 'aditya' in query:
            if lang == 'hindi':
                responses = [
                    "Shri Aditya Shrivastava hamare President aur Co-Founder hain. Ve strategic vision aur governance handle karte hain.",
                    "Aditya ji Pushpak O2 ke President hain. Company ki strategic direction ve dekhte hain.",
                    "Mr. Aditya Shrivastava hamare mukhya neta hain, President ke roop mein governance ka kaam karte hain."
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
                    "Shri Aneerudh Kumar hamare Co-Founder aur Technology Lead hain. Ve engineering aur systems architecture dekhte hain.",
                    "Aneerudh ji technical operations handle karte hain. Ve hamare Technology Lead hain.",
                    "Mr. Aneerudh Kumar engineering ka poora kaam dekhte hain, Co-Founder bhi hain."
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
                    "Pushpak O2 ke do co-founders hain - Mr. Aditya Shrivastava jo President hain aur Mr. Aneerudh Kumar jo Technology Lead hain. Dono milkar company ko chala rahe hain.",
                    "Pushpak auto yaani Pushpak O2 ke founders hain Aditya Shrivastava sahab (President) aur Aneerudh Kumar ji (Technology Lead). Dono co-founders hain.",
                    "Hamare company ke do mukhya neta hain - Aditya ji jo business operations handle karte hain aur Aneerudh ji jo technical work dekhte hain."
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
                    "Pushpak O2 ke do co-founders hain - Mr. Aditya Shrivastava (President) aur Mr. Aneerudh Kumar (Technology Lead). Dono milkar company ko aage badha rahe hain.",
                    "Hamare founders hain Aditya ji jo business operations handle karte hain aur Aneerudh ji jo technical side dekhte hain.",
                    "Company ke do mukhya neta hain - strategic leadership ke liye Aditya Shrivastava aur technical innovation ke liye Aneerudh Kumar."
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
                    "Pushpak O2 ka headquarters Bhopal, Madhya Pradesh mein hai.",
                    "Hamara mukhyalay Bhopal mein sthit hai, MP mein.",
                    "Company ka base Bhopal, Madhya Pradesh mein hai."
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
                    "Pushpak O2 ek Indian aerospace company hai jo indigenous aviation platforms aur unmanned aerial systems develop karti hai.",
                    "Yeh Bharatiya aerospace company hai jo swadeshi vimanan takneek banati hai.",
                    "Hamari company indigenous aircraft aur drone technology mein kaam karti hai."
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
        # Language is already detected, no need to override
            
        if 'capacity' in query or 'load' in query or 'person' in query:
            if lang == 'hindi':
                responses = [
                    "Pushpak vehicle ki load capacity 500kg hai ya 4 persons tak le ja sakta hai.",
                    "Yeh 4 logon ko carry kar sakta hai ya 500 kilo wajan utha sakta hai.",
                    "Ismein 4 vyakti baith sakte hain ya 500kg ka bhaar le ja sakta hai."
                ]
            else:
                responses = [
                    "Pushpak vehicle has a load capacity of 500kg or can carry up to 4 persons.",
                    "It can carry 4 people or lift 500 kilograms of weight.",
                    "The vehicle can seat 4 persons or carry a load of 500kg."
                ]
            return self.get_varied_response('capacity', responses)
        
        elif 'speed' in query or 'fast' in query or 'kitni speed' in query or 'top speed' in query or 'speeed' in query:
            # Always respond in both languages for speed queries
            return "Pushpak vehicle ki top speed 400 kilometer per hour hai. The top speed of Pushpak vehicle is 400 kilometers per hour."
            
        elif 'features' in query:
            if lang == 'hindi':
                responses = [
                    "Pushpak vehicle mein AI-enabled autonomous flight, real-time obstacle detection, hydrogen fuel cell power, aur zero-emission operations hai.",
                    "Ismein swachalit udaan, baadha pehchaan, hydrogen indhan aur shunya pradooshan ki suvidha hai.",
                    "Vehicle mein AI flight control, obstacle avoidance, hydrogen power aur eco-friendly operations hain."
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
                    "Pushpak ek advanced unmanned aerial system hai with hybrid capabilities aur DGCA compliant design.",
                    "Yeh ek unnat drone hai jo hybrid technology aur DGCA maankon ke anusaar bana hai.",
                    "Pushpak aerial vehicle ek smart UAS hai jo sabhi aviation niyamon ka paalan karta hai."
                ]
            else:
                responses = [
                    "Pushpak is an advanced unmanned aerial system with hybrid capabilities and DGCA compliant design.",
                    "It is an advanced drone built with hybrid technology and DGCA standards.",
                    "Pushpak aerial vehicle is a smart UAS that complies with all aviation regulations."
                ]
            return self.get_varied_response('vehicle_general', responses)
    
    def get_weather_info(self, query, lang):
        """Get weather information based on query"""
        # Check if asking for forecast/tomorrow
        if 'forecast' in query or 'kal' in query or 'tomorrow' in query:
            forecast = self.weather_service.get_forecast(lang)
            if forecast:
                return forecast
            else:
                if lang == 'hindi':
                    return "Maaf kijiye, mausam ki jaankari abhi nahi mil pa rahi hai."
                else:
                    return "Sorry, weather information is not available right now."
        # Default: return today's weather for any weather keyword
        else:
            weather = self.weather_service.get_weather(lang)
            if weather:
                return weather
            else:
                if lang == 'hindi':
                    return "Maaf kijiye, mausam ki jaankari abhi nahi mil pa rahi hai."
                else:
                    return "Sorry, weather information is not available right now."
    
    def chat(self, user_input):
        """Main chat function that analyzes and responds"""
        # Remove name prefix if present
        cleaned_input = self.remove_name_prefix(user_input)
        return self.analyze_query(cleaned_input)
    
    def remove_name_prefix(self, text):
        """Remove 'Shipra' or similar name prefixes from input"""
        # Common name patterns
        name_patterns = ['shipra', 'shipra ji', 'hey shipra', 'hi shipra', 'hello shipra']
        
        text_lower = text.lower().strip()
        
        for pattern in name_patterns:
            if text_lower.startswith(pattern):
                # Remove the name and any following comma or whitespace
                remaining = text[len(pattern):].lstrip(' ,').strip()
                return remaining if remaining else text
        
        return text