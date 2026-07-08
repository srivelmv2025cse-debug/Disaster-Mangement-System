from pymongo import MongoClient
from django.conf import settings
from datetime import datetime

class MongoDBManager:
    def __init__(self):
        try:
            self.client = MongoClient(
                settings.MONGO_URI,
                serverSelectionTimeoutMS=3000,
                connectTimeoutMS=3000
            )
            self.db = self.client[settings.MONGO_DB_NAME]
            # Quick connectivity test
            self.client.server_info()
            self.connected = True
            print("[OK] MongoDB connected successfully")
        except Exception as e:
            print(f"[WARN] MongoDB not available: {e}")
            self.client = None
            self.db = None
            self.connected = False

    def get_collection(self, name):
        if self.db is not None:
            return self.db[name]
        return None

    def save_search_history(self, city):
        try:
            col = self.get_collection('search_history')
            if col is not None:
                col.insert_one({
                    'city': city,
                    'timestamp': datetime.now()
                })
        except Exception as e:
            print(f"MongoDB write error: {e}")

    def get_search_history(self, limit=50):
        try:
            col = self.get_collection('search_history')
            if col is not None:
                return list(col.find().sort('timestamp', -1).limit(limit))
        except Exception as e:
            print(f"MongoDB read error: {e}")
        return []

    def log_api_call(self, api_name, status, endpoint):
        try:
            col = self.get_collection('weather_api_logs')
            if col is not None:
                col.insert_one({
                    'api_name': api_name,
                    'endpoint': endpoint,
                    'status': status,
                    'timestamp': datetime.now()
                })
        except Exception as e:
            print(f"MongoDB write error: {e}")

    def save_disaster_events(self, events):
        try:
            col = self.get_collection('disaster_events')
            if col is not None:
                col.delete_many({})
                if events:
                    col.insert_many(events)
        except Exception as e:
            print(f"MongoDB write error: {e}")

    def get_disaster_events(self):
        try:
            col = self.get_collection('disaster_events')
            if col is not None:
                return list(col.find().sort('date', -1))
        except Exception as e:
            print(f"MongoDB read error: {e}")
        return []

mongo_db = MongoDBManager()
