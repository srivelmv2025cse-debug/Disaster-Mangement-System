import pandas as pd
import numpy as np
import os
from datetime import datetime
from django.conf import settings
from .mongodb import mongo_db

CSV_PATH = os.path.join(settings.BASE_DIR, 'weather_disaster_data.csv')

def load_weather_data():
    """Load the local CSV file using Pandas"""
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame()
    return pd.read_csv(CSV_PATH)

def preprocess_weather_data(df):
    """Clean and preprocess the dataset"""
    if df.empty:
        return df
    
    # Handle missing values
    df = df.dropna(subset=['city', 'temperature', 'rainfall'])
    
    # Remove duplicate records
    df = df.drop_duplicates()
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Ensure numeric columns
    numeric_cols = ['temperature', 'humidity', 'rainfall', 'wind_speed', 'pressure', 'river_level', 'soil_moisture']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Fill remaining NaNs in numeric with median
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    
    # Create derived columns like risk_score
    risk_mapping = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}
    df['risk_score'] = df['disaster_risk_level'].map(risk_mapping).fillna(1)
    
    # Season derived column
    def get_season(month):
        if month in [12, 1, 2]: return 'Winter'
        elif month in [3, 4, 5]: return 'Spring'
        elif month in [6, 7, 8]: return 'Summer'
        else: return 'Autumn'
    df['season'] = df['month'].apply(get_season)

    return df

def detect_risk_level(df):
    """Real-World Intelligence Features: Re-evaluates risk levels based on rules"""
    if df.empty: return df
    df = df.copy()
    
    df['detected_risk'] = 'Normal'
    
    # Detect flood risk
    df.loc[(df['rainfall'] > 100) & (df['river_level'] > 8), 'detected_risk'] = 'Flood Risk (Critical)'
    
    # Detect heatwave risk
    df.loc[(df['temperature'] > 38) & (df['humidity'] > 60), 'detected_risk'] = 'Heatwave Risk (High)'
    
    # Detect storm risk
    df.loc[(df['wind_speed'] > 80) & (df['pressure'] < 1000), 'detected_risk'] = 'Storm Risk (High)'
    
    # Detect drought risk
    df.loc[(df['rainfall'] < 5) & (df['soil_moisture'] < 20), 'detected_risk'] = 'Drought Risk (Medium)'
    
    return df

def generate_summary_cards(df):
    if df.empty:
        return {}
    
    summary = {
        'total_records': len(df),
        'avg_temperature': round(df['temperature'].mean(), 1),
        'total_rainfall': round(df['rainfall'].sum(), 1),
        'high_risk_alerts': len(df[df['disaster_risk_level'].isin(['High', 'Critical'])]),
        'critical_disaster_count': len(df[df['disaster_risk_level'] == 'Critical']),
        'most_affected_city': df[df['disaster_type'] != 'None']['city'].mode()[0] if not df[df['disaster_type'] != 'None'].empty else "N/A",
        'avg_wind_speed': round(df['wind_speed'].mean(), 1),
        'avg_humidity': round(df['humidity'].mean(), 1)
    }
    return summary

def generate_chart_data(df):
    """Generates aggregates required for Chart.js/Plotly"""
    if df.empty: return {}
    
    # 1. Line Chart – Monthly temperature trend
    monthly_temp = df.groupby('month')['temperature'].mean().round(1).to_dict()
    
    # 2. Bar Chart – City-wise rainfall comparison
    city_rainfall = df.groupby('city')['rainfall'].mean().round(1).sort_values(ascending=False).head(10).to_dict()
    
    # 3. Pie Chart – Disaster type distribution
    disaster_dist = df[df['disaster_type'] != 'None']['disaster_type'].value_counts().to_dict()
    
    # 4. Donut Chart – Risk level distribution
    risk_dist = df['disaster_risk_level'].value_counts().to_dict()
    
    # 5. Alert Status Analysis
    alert_dist = df['alert_status'].value_counts().to_dict()

    # 6. Weather Condition Frequency
    weather_cond = df['weather_condition'].value_counts().to_dict()

    # 7. Scatter/Correlation points (sample for frontend)
    scatter_df = df[['rainfall', 'river_level']].dropna()
    if len(scatter_df) > 100:
        scatter_df = scatter_df.sample(100, random_state=42)
    scatter_data = scatter_df.to_dict(orient='records')
    
    # 8. Stacked Bar Chart – City vs disaster risk level (top 5 cities)
    top_cities = df['city'].value_counts().head(5).index
    city_risk = df[df['city'].isin(top_cities)].groupby(['city', 'disaster_risk_level']).size().unstack(fill_value=0).to_dict(orient='index')

    return {
        'monthly_temp': monthly_temp,
        'city_rainfall': city_rainfall,
        'disaster_dist': disaster_dist,
        'risk_dist': risk_dist,
        'alert_dist': alert_dist,
        'weather_cond': weather_cond,
        'scatter_data': scatter_data,
        'city_risk': city_risk
    }

def analyze_weather_patterns(df):
    # Additional deeper analysis if needed
    pass

def analyze_disaster_patterns(df):
    # Additional deeper analysis if needed
    pass

def save_analysis_to_mongodb(summary_data, chart_data):
    """Save processed results to MongoDB"""
    try:
        col = mongo_db.get_collection('dashboard_reports')
        if col is not None:
            report = {
                'timestamp': datetime.now(),
                'summary': summary_data,
            }
            col.insert_one(report)
    except Exception as e:
        print(f'MongoDB save error: {e}')

def get_full_dashboard_data(city_filter=None, risk_filter=None, disaster_filter=None):
    df = load_weather_data()
    df = preprocess_weather_data(df)
    df = detect_risk_level(df)
    
    # Apply filters
    if city_filter:
        df = df[df['city'].str.lower() == city_filter.lower()]
    if risk_filter:
        df = df[df['disaster_risk_level'].str.lower() == risk_filter.lower()]
    if disaster_filter:
        df = df[df['disaster_type'].str.lower() == disaster_filter.lower()]

    summary = generate_summary_cards(df)
    charts = generate_chart_data(df)
    
    # Optionally save to mongo (maybe only on full data)
    if not (city_filter or risk_filter or disaster_filter):
        save_analysis_to_mongodb(summary, charts)
        
    return {
        'summary': summary,
        'charts': charts
    }
