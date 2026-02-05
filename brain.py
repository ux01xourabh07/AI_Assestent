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
        hindi_chars = len(re.findall(r'[\u0900-\u097F]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        return 'hindi' if hindi_chars > english_chars else 'english'
    
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
        lang = self.detect_language(user_input)
        
        # Company-related queries
        if any(word in query for word in ['company', 'pushpak o2', 'pushpak auto', 'leadership', 'president', 'aditya', 'aneerudh', 'location', 'bhopal', 'mission', 'founder', 'co-founder', 'kaun hai', 'who is']):
            return self.get_company_info(query, lang)
        
        # Vehicle-related queries  
        elif any(word in query for word in ['vehicle', 'pushpak', 'aerial', 'drone', 'uas', 'features', 'technology', 'hydrogen', 'autonomous', 'capacity', 'load']):
            return self.get_vehicle_info(query, lang)
        
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
                        "Koi baat nahi! Khushi se madad ki.",
                        "Welcome hai! Aur kuch chahiye?",
                        "Dhanyawad aapka! Kuch aur poochna hai?"
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
                        "Suprabhat! Aaj kaise madad kar sakti hun?",
                        "Good morning! Din shubh ho, kya chahiye?",
                        "Namaskar! Subah ki shuruaat kaise karein?"
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
                        "Namaskar! Dopahar kaisi ja rahi hai?",
                        "Good afternoon! Kaise sahayata karun?",
                        "Pranam! Din kaisa chal raha hai?"
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
                        "Shubh sandhya! Shaam kaisi hai?",
                        "Good evening! Kaise madad karun?",
                        "Namaskar! Sandhya ki shuruaat acchi ho!"
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
                        "Namaste! Main Shipra hun, Pushpak O2 ki AI assistant. Kaise help kar sakti hun?",
                        "Hello! Shipra here, aapki service mein. Kya chahiye?",
                        "Namaskar! Main Pushpak O2 ki assistant Shipra. Batao kaise madad karun?"
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
                    "Dhanyawad! Phir milte hain.",
                    "Accha, phir baat karte hain. Namaste!",
                    "Theek hai, alvida! Khush rahiye."
                ]
            return self.get_varied_response('goodbye', responses)
        
        else:
            return self.get_unknown_response(lang)
    
    def get_company_info(self, query, lang):
        """Extract specific company information based on query"""
        if 'president' in query or 'aditya' in query:
            if lang == 'hindi':
                responses = [
                    "श्री आदित्य श्रीवास्तव हमारे President और Co-Founder हैं। वे strategic vision और governance handle करते हैं।",
                    "आदित्य जी Pushpak O2 के President हैं। Company की strategic direction वे देखते हैं।",
                    "Mr. Aditya Shrivastava हमारे मुख्य नेता हैं, President के रूप में governance का काम करते हैं।"
                ]
            else:
                responses = [
                    "Mr. Aditya Shrivastava hamare President aur Co-Founder hain. Woh strategic vision aur governance handle karte hain.",
                    "Aditya ji Pushpak O2 ke President hain. Company ki strategic direction woh dekhte hain.",
                    "Aditya Shrivastava sahab hamare chief leader hain, governance ka kaam karte hain."
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
                    "Mr. Aneerudh Kumar hamare Co-Founder aur Technology Lead hain. Woh engineering aur systems architecture dekhte hain.",
                    "Aneerudh ji technical operations handle karte hain. Woh hamare Technology Lead hain.",
                    "Aneerudh Kumar sahab engineering ka poora kaam dekhte hain, Co-Founder bhi hain."
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
                    "Pushpak O2 ke do co-founders hain - Mr. Aditya Shrivastava jo President hain aur Mr. Aneerudh Kumar jo Technology Lead hain. Dono milkar company ko chala rahe hain.",
                    "Pushpak auto yaani Pushpak O2 ke founders hain Aditya Shrivastava sahab (President) aur Aneerudh Kumar ji (Technology Lead). Dono co-founders hain.",
                    "Hamare company ke do mukhya neta hain - Aditya ji jo business operations handle karte hain aur Aneerudh ji jo technical work dekhte hain."
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
                    "Pushpak O2 ke do co-founders hain - Mr. Aditya Shrivastava (President) aur Mr. Aneerudh Kumar (Technology Lead). Dono milkar company ko aage badha rahe hain.",
                    "Hamare founders hain Aditya ji jo business operations handle karte hain aur Aneerudh ji jo technical side dekhte hain.",
                    "Company ke do mukhya neta hain - strategic leadership ke liye Aditya Shrivastava aur technical innovation ke liye Aneerudh Kumar."
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
                    "Pushpak O2 ka headquarters Bhopal, Madhya Pradesh mein hai.",
                    "Hamara mukhyalay Bhopal mein sthit hai, MP mein.",
                    "Company ka base Bhopal, Madhya Pradesh mein hai."
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
                    "Pushpak O2 ek Indian aerospace company hai jo indigenous aviation platforms aur unmanned aerial systems develop karti hai.",
                    "Yah Bharatiya aerospace company hai jo swadeshi vimanan takneek banati hai.",
                    "Hamari company indigenous aircraft aur drone technology mein kaam karti hai."
                ]
            return self.get_varied_response('company_general', responses)
    
    def get_vehicle_info(self, query, lang):
        """Extract specific vehicle information based on query"""
        if 'capacity' in query or 'load' in query or 'person' in query:
            if lang == 'hindi':
                responses = [
                    "Pushpak vehicle की load capacity 500kg है या 4 persons तक ले जा सकता है।",
                    "यह 4 लोगों को carry कर सकता है या 500 किलो वजन उठा सकता है।",
                    "इसमें 4 व्यक्ति बैठ सकते हैं या 500kg का भार ले जा सकता है।"
                ]
            else:
                responses = [
                    "Pushpak vehicle ki load capacity 500kg hai ya 4 persons tak le ja sakta hai.",
                    "Yah 4 logon ko carry kar sakta hai ya 500 kilo weight utha sakta hai.",
                    "Ismein 4 vyakti baith sakte hain ya 500kg ka bhar le ja sakta hai."
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
                    "Pushpak vehicle mein AI-enabled autonomous flight, real-time obstacle detection, hydrogen fuel cell power, aur zero-emission operations hai.",
                    "Ismein swachalit udan, badha pahchan, hydrogen fuel aur shunya pradooshan ki suvidha hai.",
                    "Vehicle mein AI flight control, obstacle avoidance, hydrogen power aur eco-friendly operations hain."
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
                    "Pushpak ek advanced unmanned aerial system hai with hybrid capabilities aur DGCA compliant design.",
                    "Yah ek unnat drone hai jo hybrid technology aur DGCA mankon ke anusar bana hai.",
                    "Pushpak aerial vehicle ek smart UAS hai jo sabhi aviation niyamon ka palan karta hai."
                ]
            return self.get_varied_response('vehicle_general', responses)
    
    def chat(self, user_input):
        """Main chat function that analyzes and responds"""
        return self.analyze_query(user_input)