# 🌍 Weather & Disaster Forecast Analysis System

A professional, django-based analytics and forecasting system designed to monitor real-time weather conditions, track global natural disasters, and perform advanced statistical data processing.

The interface features a **premium glassmorphism dark mode design** with rich interactive visualizations powered by Chart.js and Plotly.

---

## 🚀 Key Features

* **Premium Analytics Dashboard**: A sleek, modern dark-themed user interface utilizing glassmorphism aesthetics.
* **Real-time API Integrations**:
  * **Open-Meteo Geocoding & Weather APIs**: Fetches real-time temperatures, relative humidity, wind speed, weather codes, and 24-hour forecasts for any city worldwide.
  * **NASA EONET API**: Feeds real-time data on active global natural disasters (fires, storms, volcanoes, floods).
  * **Google News RSS Feed**: Displays the latest headlines and articles related to weather anomalies and disasters.
* **Advanced Data Processing**:
  * Powered by **Pandas & NumPy** to clean and process a pre-loaded local dataset of **1,500+ records**.
  * Dynamic filtering on the dashboard by City, Risk Level, and Disaster Type.
* **Interactive Visualizations**:
  * **Chart.js**: Rendered line charts for monthly temperature trends, bar charts for rainfall comparisons, and donut charts for disaster risk levels.
  * **Plotly**: Geospatial analysis and scatter plot representing the correlation between rainfall and river levels.
* **MongoDB Integration**: Logs search queries, caches disaster events, and maintains API call status logs.

---

## 🛠️ Technology Stack

* **Backend**: Django 6.x (Python 3.14+)
* **Database**: MongoDB (via PyMongo client)
* **Data Processing**: Pandas, NumPy
* **Frontend**: HTML5, Vanilla CSS3 (Custom Glassmorphism styling), Vanilla JavaScript
* **Charts**: Chart.js, Plotly.js

---

## 📦 Directory Structure

```text
weather_disaster_analysis/
│
├── weather_project/            # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
│
├── dashboard/                  # Core Django application
│   ├── analytics.py            # Pandas/NumPy data processing engine
│   ├── api_services.py        # Integration with external APIs (Open-Meteo, NASA, News)
│   ├── mongodb.py              # MongoDB manager & query helper
│   ├── views.py                # Django views and API endpoints
│   └── urls.py                 # App routing
│
├── templates/                  # HTML templates
│   ├── base.html               # Main layout skeleton
│   ├── home.html               # Dashboard home
│   ├── live_weather.html       # Real-time search & 24hr forecast
│   ├── disasters.html          # NASA EONET disaster tracker
│   └── analytics.html          # Dynamic analytics & report filters
│
├── static/                     # Static assets
│   ├── css/style.css           # Premium glassmorphism dark theme CSS
│   └── js/
│       ├── dashboard.js        # Core helper scripts & DOM actions
│       └── charts.js           # Chart.js & Plotly visualizers
│
├── generate_data.py            # Local dataset generator (1500+ records)
├── weather_disaster_data.csv   # Generated CSV dataset
└── requirements.txt            # Python dependencies list
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/srivelmv2025cse-debug/Disaster-Mangement-System.git
cd Disaster-Mangement-System
```

### 2. Set Up Virtual Environment & Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Start MongoDB
Ensure MongoDB is running locally on your default port: `mongodb://localhost:27017/`.  
*Note: The application will automatically detect if MongoDB is offline and run in a graceful offline mode, fallback configurations are implemented.*

### 4. Populate Local Dataset (Optional)
To generate or refresh the local dataset of 1,550 records, run:
```bash
python generate_data.py
```

### 5. Start the Server
Run Django check and boot up the development server:
```bash
python manage.py check
python manage.py runserver
```
Visit the dashboard at `http://127.0.0.1:8000/` in your browser.
