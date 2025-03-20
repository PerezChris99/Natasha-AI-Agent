import requests
from datetime import datetime
import os

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                return (f"Current weather in {city}: "
                       f"{data['weather'][0]['description']}, "
                       f"Temperature: {data['main']['temp']}°C, "
                       f"Humidity: {data['main']['humidity']}%")
            return "Sorry, I couldn't fetch the weather information."
        except Exception as e:
            return f"Error getting weather: {str(e)}"
