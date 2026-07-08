import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_data(num_records=1550):
    cities = [
        {"city": "New York", "state": "New York", "country": "USA", "lat": 40.7128, "lon": -74.0060},
        {"city": "Los Angeles", "state": "California", "country": "USA", "lat": 34.0522, "lon": -118.2437},
        {"city": "London", "state": "England", "country": "UK", "lat": 51.5074, "lon": -0.1278},
        {"city": "Tokyo", "state": "Tokyo", "country": "Japan", "lat": 35.6762, "lon": 139.6503},
        {"city": "Sydney", "state": "NSW", "country": "Australia", "lat": -33.8688, "lon": 151.2093},
        {"city": "Mumbai", "state": "Maharashtra", "country": "India", "lat": 19.0760, "lon": 72.8777},
        {"city": "Rio de Janeiro", "state": "Rio de Janeiro", "country": "Brazil", "lat": -22.9068, "lon": -43.1729},
        {"city": "Cairo", "state": "Cairo", "country": "Egypt", "lat": 30.0444, "lon": 31.2357},
        {"city": "Paris", "state": "Ile-de-France", "country": "France", "lat": 48.8566, "lon": 2.3522},
        {"city": "Toronto", "state": "Ontario", "country": "Canada", "lat": 43.6510, "lon": -79.3470},
        {"city": "Beijing", "state": "Beijing", "country": "China", "lat": 39.9042, "lon": 116.4074},
        {"city": "Moscow", "state": "Moscow", "country": "Russia", "lat": 55.7558, "lon": 37.6173},
        {"city": "Cape Town", "state": "Western Cape", "country": "South Africa", "lat": -33.9249, "lon": 18.4241},
        {"city": "Dubai", "state": "Dubai", "country": "UAE", "lat": 25.2048, "lon": 55.2708},
        {"city": "Singapore", "state": "Singapore", "country": "Singapore", "lat": 1.3521, "lon": 103.8198}
    ]

    weather_conditions = ["Clear", "Cloudy", "Rain", "Snow", "Thunderstorm", "Fog"]
    disaster_types = ["Flood", "Heatwave", "Storm", "Drought", "Cyclone", "Landslide", "None"]
    risk_levels = ["Low", "Medium", "High", "Critical"]
    alert_statuses = ["Normal", "Watch", "Warning", "Emergency"]
    response_actions = ["No Action", "Monitor", "Alert Public", "Evacuation Support"]

    start_date = datetime(2023, 1, 1)

    data = []
    for i in range(num_records):
        city_info = random.choice(cities)
        record_date = start_date + timedelta(days=random.randint(0, 365*2))
        
        # Base realistic values based on some logic (or just random for this dataset)
        temp = round(random.uniform(-10.0, 45.0), 1)
        humidity = random.randint(10, 100)
        rainfall = round(random.uniform(0.0, 200.0), 1)
        wind_speed = round(random.uniform(0.0, 120.0), 1)
        pressure = random.randint(950, 1050)
        river_level = round(random.uniform(0.5, 10.0), 1)
        soil_moisture = random.randint(5, 95)
        
        # Adjust disaster type based on temp/rainfall to make analysis somewhat realistic
        if rainfall > 100 and river_level > 8:
            disaster = "Flood"
        elif temp > 38 and humidity > 60:
            disaster = "Heatwave"
        elif wind_speed > 80:
            disaster = random.choice(["Storm", "Cyclone"])
        elif rainfall < 5 and temp > 30 and soil_moisture < 20:
            disaster = "Drought"
        elif rainfall > 50 and random.random() > 0.8:
            disaster = "Landslide"
        else:
            disaster = "None" if random.random() > 0.3 else random.choice([d for d in disaster_types if d != "None"])

        if disaster == "None":
            risk = "Low"
            alert = "Normal"
            action = "No Action"
        else:
            risk = random.choice(["Medium", "High", "Critical"])
            if risk == "Medium":
                alert = "Watch"
                action = "Monitor"
            elif risk == "High":
                alert = "Warning"
                action = "Alert Public"
            else:
                alert = "Emergency"
                action = "Evacuation Support"

        # Override some weather condition based on disaster
        if disaster == "Flood" or disaster == "Storm" or disaster == "Cyclone":
            condition = "Thunderstorm" if random.random() > 0.5 else "Rain"
        elif disaster == "Heatwave" or disaster == "Drought":
            condition = "Clear"
        else:
            condition = random.choice(weather_conditions)

        data.append({
            "record_id": f"REC_{1000 + i}",
            "date": record_date.strftime("%Y-%m-%d"),
            "year": record_date.year,
            "month": record_date.month,
            "city": city_info["city"],
            "state": city_info["state"],
            "country": city_info["country"],
            "latitude": city_info["lat"],
            "longitude": city_info["lon"],
            "temperature": temp,
            "humidity": humidity,
            "rainfall": rainfall,
            "wind_speed": wind_speed,
            "pressure": pressure,
            "weather_condition": condition,
            "disaster_type": disaster,
            "disaster_risk_level": risk,
            "river_level": river_level,
            "soil_moisture": soil_moisture,
            "alert_status": alert,
            "response_action": action
        })

    df = pd.DataFrame(data)
    df.to_csv("weather_disaster_data.csv", index=False)
    print(f"Successfully generated {len(df)} records to weather_disaster_data.csv")

if __name__ == "__main__":
    generate_data()
