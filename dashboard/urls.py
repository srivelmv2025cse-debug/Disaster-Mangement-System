from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.home, name='home'),
    path('live-weather/', views.live_weather, name='live_weather'),
    path('disasters/', views.disasters, name='disasters'),
    path('analytics/', views.analytics, name='analytics'),
    path('history/', views.history, name='history'),
    path('reports/', views.reports, name='reports'),
    
    # API endpoints
    path('api/weather/', views.api_weather, name='api_weather'),
    path('api/disasters/', views.api_disasters, name='api_disasters'),
    path('api/news/', views.api_news, name='api_news'),
    path('api/search-history/', views.api_search_history, name='api_search_history'),
    path('api/dashboard-data/', views.api_dashboard_data, name='api_dashboard_data'),
]
