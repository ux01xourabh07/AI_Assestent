import requests
import geocoder

class WeatherService:
    def __init__(self):
        self.base_url = "https://wttr.in"
    
    def get_location(self):
        """Get user's location based on IP"""
        try:
            g = geocoder.ip('me')
            if g.ok:
                return g.city, g.country
            return None, None
        except:
            return None, None
    
    def get_weather(self, lang='english'):
        """Get current weather for user's location"""
        try:
            city, country = self.get_location()
            if not city:
                city = "Bhopal"  # Default to Pushpak O2 location
            
            # Get weather data in JSON format
            response = requests.get(f"{self.base_url}/{city}?format=j1", timeout=5)
            if response.status_code != 200:
                return None
            
            data = response.json()
            current = data['current_condition'][0]
            
            temp_c = current['temp_C']
            feels_like = current['FeelsLikeC']
            humidity = current['humidity']
            weather_desc = current['weatherDesc'][0]['value']
            
            # Format response based on language
            if lang == 'hindi':
                return (f"{city} mein abhi temperature {temp_c} degree hai. "
                       f"Mahsoos {feels_like} degree jaisa ho raha hai. "
                       f"Mausam {weather_desc} hai aur humidity {humidity} percent hai.")
            else:
                return (f"In {city}, the temperature is {temp_c} degrees Celsius. "
                       f"It feels like {feels_like} degrees. "
                       f"Weather is {weather_desc} with {humidity}% humidity.")
        except:
            return None
    
    def get_forecast(self, lang='english'):
        """Get weather forecast"""
        try:
            city, _ = self.get_location()
            if not city:
                city = "Bhopal"
            
            response = requests.get(f"{self.base_url}/{city}?format=j1", timeout=5)
            if response.status_code != 200:
                return None
            
            data = response.json()
            tomorrow = data['weather'][1] if len(data['weather']) > 1 else data['weather'][0]
            
            max_temp = tomorrow['maxtempC']
            min_temp = tomorrow['mintempC']
            desc = tomorrow['hourly'][0]['weatherDesc'][0]['value']
            
            if lang == 'hindi':
                return (f"Kal ka mausam {desc} rahega. "
                       f"Temperature {min_temp} se {max_temp} degree ke beech rahega.")
            else:
                return (f"Tomorrow's weather will be {desc}. "
                       f"Temperature will range from {min_temp} to {max_temp} degrees.")
        except:
            return None
