import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def get_weather_data(city):
    """Fetch weather data from Open-Meteo API"""
    try:
        # Geocode the city
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_response = requests.get(geocode_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data.get('results'):
            return None, "City not found"
            
        location = geo_data['results'][0]
        lat = location['latitude']
        lon = location['longitude']
        country = location.get('country', '')
        
        # Get weather data
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&forecast_days=2&timezone=auto"
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        current = weather_data.get('current', {})
        hourly = weather_data.get('hourly', {})
        
        # Get next 24 hours of data
        times = hourly.get('time', [])[:24]
        temps = hourly.get('temperature_2m', [])[:24]
        hums = hourly.get('relative_humidity_2m', [])[:24]
        winds = hourly.get('wind_speed_10m', [])[:24]
        
        return {
            'city': location['name'],
            'country': country,
            'temperature': current.get('temperature_2m'),
            'humidity': current.get('relative_humidity_2m'),
            'wind_speed': current.get('wind_speed_10m'),
            'weather_code': current.get('weather_code'),
            'forecast': {
                'times': times,
                'temperatures': temps,
                'humidities': hums,
                'wind_speeds': winds
            }
        }, None

    except requests.exceptions.RequestException as e:
        return None, str(e)

def get_disasters():
    """Fetch global disasters from NASA EONET"""
    disaster_url = "https://eonet.gsfc.nasa.gov/api/v3/events?limit=8&status=open"
    try:
        response = requests.get(disaster_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        events = data.get('events', [])
        
        simplified_events = []
        for event in events:
            simplified_events.append({
                'title': event.get('title'),
                'categories': [c.get('title') for c in event.get('categories', [])],
                'date': event.get('geometry', [{}])[0].get('date', 'Unknown Date')
            })
            
        return simplified_events, None
    except requests.exceptions.RequestException as e:
        return [], str(e)

def get_news():
    """Fetch weather and disaster news from Google RSS"""
    try:
        url = "https://news.google.com/rss/search?q=weather+disaster&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        news_items = []
        for item in root.findall('.//item')[:6]:
            news_items.append({
                'title': item.find('title').text,
                'link': item.find('link').text,
                'pubDate': item.find('pubDate').text
            })
        return news_items, None
    except Exception as e:
        return [], str(e)
