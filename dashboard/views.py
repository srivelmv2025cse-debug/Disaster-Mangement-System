from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from .api_services import get_weather_data, get_disasters, get_news
from .mongodb import mongo_db
from .analytics import get_full_dashboard_data

def home(request):
    return render(request, 'home.html')

def live_weather(request):
    return render(request, 'live_weather.html')

def disasters(request):
    return render(request, 'disasters.html')

def analytics(request):
    return render(request, 'analytics.html')

def history(request):
    return render(request, 'history.html')

def reports(request):
    return render(request, 'reports.html')

# API Endpoints
@csrf_exempt
def api_weather(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            city = data.get('city')
            if not city:
                return JsonResponse({'error': 'City is required'}, status=400)
                
            mongo_db.save_search_history(city)
            weather_data, error = get_weather_data(city)
            
            if error:
                mongo_db.log_api_call('Open-Meteo', 'failed', '/v1/forecast')
                return JsonResponse({'error': error}, status=500)
                
            mongo_db.log_api_call('Open-Meteo', 'success', '/v1/forecast')
            return JsonResponse(weather_data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid method'}, status=405)

def api_disasters(request):
    events, error = get_disasters()
    if error:
        mongo_db.log_api_call('NASA-EONET', 'failed', '/api/v3/events')
        return JsonResponse({'error': error}, status=500)
        
    mongo_db.log_api_call('NASA-EONET', 'success', '/api/v3/events')
    mongo_db.save_disaster_events(events)
    return JsonResponse({'events': events})

def api_news(request):
    news, error = get_news()
    if error:
        return JsonResponse({'error': error}, status=500)
    return JsonResponse({'news': news})

def api_search_history(request):
    history_data = mongo_db.get_search_history()
    # convert ObjectIds and datetime to string
    for item in history_data:
        item['_id'] = str(item['_id'])
        if 'timestamp' in item and isinstance(item['timestamp'], datetime):
            item['timestamp'] = item['timestamp'].isoformat()
    return JsonResponse({'history': history_data})

def api_dashboard_data(request):
    """Returns analytics data (summary and charts) with optional filters"""
    city = request.GET.get('city')
    risk = request.GET.get('risk_level')
    disaster = request.GET.get('disaster_type')
    
    try:
        data = get_full_dashboard_data(city_filter=city, risk_filter=risk, disaster_filter=disaster)
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
