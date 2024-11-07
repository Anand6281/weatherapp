from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('map/', views.map, name='map'),
    path('alerts/', views.alerts, name='alerts'),
    path('alerts/delete/<int:alert_id>/', views.delete_alert, name='delete-alert'),
    path('preferences/', views.preferences, name='preferences'),
    path('weather/get/', views.get_weather, name='get-weather'),
    path('weather/forecast/', views.get_weather_forecast, name='weather_forecast'),
]