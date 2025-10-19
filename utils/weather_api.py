"""
Weather API integration
"""
import requests
import random
from datetime import datetime, timedelta

class WeatherAPI:
    """
    Weather data fetcher
    For demo purposes, uses simulated data
    For production, integrate with OpenWeatherMap API
    """
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def fetch_weather(self, location):
        """
        Fetch weather data for a location
        
        Parameters:
        -----------
        location : str
            City or state name
            
        Returns:
        --------
        dict : Weather data including temperature, humidity, rainfall
        """
        # For demo: Generate simulated weather data
        # In production, uncomment the real API call below
        
        return self._generate_mock_weather(location)
        
        # REAL API CALL (uncomment when you have API key):
        # if not self.api_key:
        #     return self._generate_mock_weather(location)
        # 
        # try:
        #     params = {
        #         'q': location + ',IN',
        #         'appid': self.api_key,
        #         'units': 'metric'
        #     }
        #     response = requests.get(self.base_url, params=params, timeout=5)
        #     
        #     if response.status_code == 200:
        #         data = response.json()
        #         return self._parse_weather_response(data)
        #     else:
        #         return self._generate_mock_weather(location)
        # 
        # except Exception as e:
        #     print(f"Error fetching weather: {e}")
        #     return self._generate_mock_weather(location)
    
    def _parse_weather_response(self, data):
        """Parse OpenWeatherMap API response"""
        return {
            'temperature': round(data['main']['temp'], 1),
            'humidity': data['main']['humidity'],
            'rainfall': data.get('rain', {}).get('1h', 0) * 30,  # Convert to monthly
            'condition': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed'],
            'pressure': data['main']['pressure']
        }
    
    def _generate_mock_weather(self, location):
        """Generate simulated weather data"""
        conditions = ['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy']
        
        # Location-based weather patterns (realistic for Indian states)
        location_patterns = {
            'West Bengal': {'temp_range': (25, 35), 'rain_range': (80, 150)},
            'Punjab': {'temp_range': (20, 38), 'rain_range': (20, 60)},
            'Maharashtra': {'temp_range': (22, 36), 'rain_range': (30, 100)},
            'Tamil Nadu': {'temp_range': (26, 38), 'rain_range': (40, 120)},
            'Kerala': {'temp_range': (24, 32), 'rain_range': (100, 200)},
        }
        
        pattern = location_patterns.get(location, {'temp_range': (20, 35), 'rain_range': (50, 120)})
        
        weather_data = {
            'temperature': round(random.uniform(*pattern['temp_range']), 1),
            'humidity': random.randint(45, 85),
            'rainfall': random.randint(*pattern['rain_range']),
            'condition': random.choice(conditions),
            'wind_speed': round(random.uniform(5, 20), 1),
            'pressure': random.randint(1000, 1020),
            'forecast': self._generate_forecast()
        }
        
        return weather_data
    
    def _generate_forecast(self):
        """Generate 5-day forecast"""
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        forecast = []
        
        base_temp = random.randint(25, 30)
        
        for i, day in enumerate(days):
            forecast.append({
                'day': day,
                'temp': base_temp + random.randint(-3, 3),
                'rain': random.randint(0, 80),
                'humidity': random.randint(50, 80)
            })
        
        return forecast


def fetch_weather_data(location):
    """
    Convenience function to fetch weather data
    
    Parameters:
    -----------
    location : str
        Location name
        
    Returns:
    --------
    dict : Weather data
    """
    weather_api = WeatherAPI()
    return weather_api.fetch_weather(location)