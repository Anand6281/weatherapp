from django.shortcuts import render, redirect
import requests, random
from django.http import JsonResponse
from django.conf import settings
from faker import Faker
from apps.main.models import HourlyForecast, WeatherForecast
from django.http import JsonResponse
from django.conf import settings
from django.core.exceptions import ValidationError
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from apps.main.forms import AlertForm
from django.contrib import messages
from apps.users.models import Alert

# Create your views here.
def home(request):
    return render(request, 'main/home.html', {
        'days': range(1, 8),
    })

def map(request):
    return render(request, 'main/map.html', {
        'hours': range(1, 7),
        'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
    })

def generate_alerts(total):
    fake = Faker()
    
    # Define possible alert types and their corresponding colors
    alert_types = [
        ('Temperature', 'red'),
        ('Rain', 'blue'),
        ('Wind', 'yellow'),
        ('Humidity', 'green'),
        ('Air Quality', 'purple')
    ]
    
    # Define possible statuses and their corresponding colors
    statuses = [
        ('Active', 'green'),
        ('Pending', 'yellow'),
        ('Resolved', 'blue'),
        ('Expired', 'gray')
    ]
    
    # Generate a list of 10 fake alerts
    alerts = []
    for i in range(total):
        alert_type, type_color = random.choice(alert_types)
        status, status_color = random.choice(statuses)
        
        alert = {
            'id': i + 1,
            'type': alert_type,
            'type_color': type_color,
            'location': fake.city(),
            'condition': generate_condition(alert_type),
            'status': status,
            'status_color': status_color
        }
        alerts.append(alert)
    
    return alerts

def generate_alert_history(total):
    fake = Faker()
    
    # Define possible alert types and their corresponding colors
    alert_types = [
        'Temperature',
        'Rain',
        'Wind',
        'Humidity',
        'Air Quality'
    ]
    
    # Define possible statuses
    statuses = ['Triggered', 'Resolved', 'Expired']
    
    # Generate a list of 50 fake alert history entries
    alert_history = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)  # Generate data for the last 30 days
    
    for i in range(total):
        alert_type = random.choice(alert_types)
        status = random.choice(statuses)
        
        alert = {
            'date': fake.date_time_between(start_date=start_date, end_date=end_date).strftime("%Y-%m-%d %H:%M:%S"),
            'type': alert_type,
            'location': fake.city(),
            'condition': generate_condition(alert_type),
            'status': status
        }
        alert_history.append(alert)
    
    # Sort the alert history by date, most recent first
    alert_history.sort(key=lambda x: x['date'], reverse=True)
    
    return alert_history


def generate_condition(alert_type):
    fake = Faker()
    
    if alert_type == 'Temperature':
        return f"{'Above' if random.choice([True, False]) else 'Below'} {fake.random_int(min=-10, max=40)}°C"
    elif alert_type == 'Rain':
        return f"{'More' if random.choice([True, False]) else 'Less'} than {fake.random_int(min=1, max=100)} mm"
    elif alert_type == 'Wind':
        return f"{'Above' if random.choice([True, False]) else 'Below'} {fake.random_int(min=0, max=100)} km/h"
    elif alert_type == 'Humidity':
        return f"{'Above' if random.choice([True, False]) else 'Below'} {fake.random_int(min=0, max=100)}%"
    elif alert_type == 'Air Quality':
        return f"AQI {'Above' if random.choice([True, False]) else 'Below'} {fake.random_int(min=0, max=500)}"
    else:
        return "Unknown condition"


def get_alert_status(forecast):
    """
    Determine alert status based on weather conditions
    """
    # Temperature alerts
    if forecast.temp_c >= 35 or forecast.temp_c <= 0:
        return 'Warning'
    
    # Rain probability alerts
    if forecast.chance_of_rain >= 70:
        return 'Warning'
    elif forecast.chance_of_rain >= 50:
        return 'Watch'
    
    # Wind alerts (wind_kph > 50 km/h is considered strong)
    if forecast.wind_kph >= 50:
        return 'Warning'
    elif forecast.wind_kph >= 30:
        return 'Watch'
    
    # Check for severe weather conditions
    severe_conditions = [
        'Thunder', 'Storm', 'Snow', 'Sleet', 'Blizzard',
        'Heavy rain', 'Thunderstorm', 'Severe'
    ]
    if any(cond in forecast.condition for cond in severe_conditions):
        return 'Warning'
    
    return 'Normal'

def alerts(request):
    form = AlertForm()
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            # Save the alert to the database
            alert = form.save(commit=False)
            alert.account = request.user
            alert.save()
            print("ALERT SAVED!")
            messages.success(request, 'Alert saved successfully')
            
            # Redirect to the alerts page
            return redirect('main:alerts')
        else:
            print("FORM INVALID")
            messages.error(request, 'Invalid form')
            print(form)
    # Get all hourly forecasts for the next 24 hours
    current_time = timezone.now()
    hourly_forecasts = HourlyForecast.objects.select_related('weather_forecast').filter(
        time__gte=current_time,
        time__lte=current_time + timezone.timedelta(hours=24)
    ).order_by('time')

    # Add alert status to each forecast
    for forecast in hourly_forecasts:
        forecast.alert_status = get_alert_status(forecast)
    
    return render(request, 'main/alerts.html', {
        'active_alerts_count': random.randint(3, 20),
        'monitored_locations_count': random.randint(5, 15),
        'recent_triggers_count': random.randint(3, 10),
        'notifications_sent_count': random.randint(7, 20),
        'alerts': Alert.objects.all(),
        'hourly_forecasts': hourly_forecasts,    
        'form': form,    
    })
    

def delete_alert(request, alert_id):
    alert = Alert.objects.get(id=alert_id)
    alert.delete()
    messages.success(request, 'Alert deleted successfully')
    return redirect('main:alerts')


def preferences(request):
    return render(request, 'main/preferences.html')

def get_weather(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    if not lat or not lon:
        return JsonResponse({'error': 'Latitude and longitude are required'}, status=400)
    
    api_key = settings.WEATHERAPI_API_KEY
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={lat},{lon}&days=7&aqi=no&alerts=no'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return JsonResponse(weather_data)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def validate_coordinates(lat, lon):
    try:
        lat_float = float(lat)
        lon_float = float(lon)
        
        if not (-90 <= lat_float <= 90):
            raise ValidationError("Latitude must be between -90 and 90")
        if not (-180 <= lon_float <= 180):
            raise ValidationError("Longitude must be between -180 and 180")
            
        return round(lat_float, 6), round(lon_float, 6)
    except (TypeError, ValueError):
        raise ValidationError("Invalid coordinates format")

def get_weather_forecast(request):
    try:
        # Get coordinates from GET request
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        
        if not lat or not lon:
            return JsonResponse({
                'error': 'Both latitude and longitude are required'
            }, status=400)
            
        # Validate coordinates
        try:
            latitude, longitude = validate_coordinates(lat, lon)
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        # Check if we have recent forecast data (less than 1 hour old)
        recent_forecast = WeatherForecast.objects.filter(
            latitude=latitude,
            longitude=longitude,
            last_updated__gte=timezone.now() - timedelta(hours=1)  # Updated line
        ).first()
        
        if recent_forecast:
            return format_forecast_response(recent_forecast)
        
        # If no recent data, fetch from API
        api_key = settings.WEATHERAPI_API_KEY
        days = 1
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={latitude},{longitude}&days={days}&aqi=yes"
        
        response = requests.get(url)
        if response.status_code != 200:
            return JsonResponse({
                'error': f'Weather API error: {response.text}'
            }, status=502)
            
        data = response.json()
        
        # Delete old forecasts for this location
        WeatherForecast.objects.filter(
            latitude=latitude,
            longitude=longitude
        ).delete()
        
        WeatherForecast.objects.all().delete()
        
        # Create or update forecast for each day
        for forecast_day in data['forecast']['forecastday']:
            weather_forecast = WeatherForecast.objects.create(
                latitude=latitude,
                longitude=longitude,
                location_name=data['location']['name'],
                date=forecast_day['date'],
                current_temp_c=data['current']['temp_c'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['avgtemp_c'],
                current_condition=data['current']['condition']['text'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['condition']['text'],
                current_condition_icon=data['current']['condition']['icon'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['condition']['icon'],
                current_wind_kph=data['current']['wind_kph'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['maxwind_kph'],
                current_wind_dir=data['current']['wind_dir'] if forecast_day['date'] == data['current']['last_updated'][:10] else "",
                current_pressure_mb=data['current']['pressure_mb'] if forecast_day['date'] == data['current']['last_updated'][:10] else 0,
                current_precip_mm=data['current']['precip_mm'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['totalprecip_mm'],
                current_humidity=data['current']['humidity'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['avghumidity'],
                current_cloud=data['current']['cloud'] if forecast_day['date'] == data['current']['last_updated'][:10] else 0,
                current_feelslike_c=data['current']['feelslike_c'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['avgtemp_c'],
                current_aqi_co=data['current']['air_quality']['co'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['air_quality']['co'],
                current_aqi_no2=data['current']['air_quality']['no2'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['air_quality']['no2'],
                current_aqi_o3=data['current']['air_quality']['o3'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['air_quality']['o3'],
                current_aqi_so2=data['current']['air_quality']['so2'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['air_quality']['so2'],
                current_aqi_pm2_5=data['current']['air_quality']['pm2_5'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['air_quality']['pm2_5'],
                current_aqi_pm10=data['current']['air_quality']['pm10'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['air_quality']['pm10'],
                current_aqi_us_epa_index=data['current']['air_quality']['us-epa-index'] if forecast_day['date'] == data['current']['last_updated'][:10] else forecast_day['day']['air_quality']['us-epa-index'],
                # Add min and max temperature fields
                min_temp_c=forecast_day['day']['mintemp_c'],
                max_temp_c=forecast_day['day']['maxtemp_c'],
            )
            
            # Create hourly forecasts
            for hour in forecast_day['hour']:
                HourlyForecast.objects.create(
                    weather_forecast=weather_forecast,
                    time=datetime.strptime(hour['time'], '%Y-%m-%d %H:%M'),
                    temp_c=hour['temp_c'],
                    condition=hour['condition']['text'],
                    condition_icon=hour['condition']['icon'],
                    wind_kph=hour['wind_kph'],
                    wind_dir=hour['wind_dir'],
                    pressure_mb=hour['pressure_mb'],
                    precip_mm=hour['precip_mm'],
                    humidity=hour['humidity'],
                    cloud=hour['cloud'],
                    feelslike_c=hour['feelslike_c'],
                    chance_of_rain=hour['chance_of_rain']
                )
        
        return format_forecast_response(weather_forecast)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def format_forecast_response(forecast):
    """Format the forecast data for the response"""
    hourly_data = forecast.hourly_forecasts.all().order_by('time')
    
    response_data = {
        'location': {
            'name': forecast.location_name,
            'latitude': str(forecast.latitude),
            'longitude': str(forecast.longitude)
        },
        'date': forecast.date,
        'current': {
            'temp_c': forecast.current_temp_c,
            'condition': forecast.current_condition,
            'condition_icon': forecast.current_condition_icon,
            'wind_kph': forecast.current_wind_kph,
            'wind_dir': forecast.current_wind_dir,
            'pressure_mb': forecast.current_pressure_mb,
            'precip_mm': forecast.current_precip_mm,
            'humidity': forecast.current_humidity,
            'cloud': forecast.current_cloud,
            'feelslike_c': forecast.current_feelslike_c,
            'air_quality': {
                'co': forecast.current_aqi_co,
                'no2': forecast.current_aqi_no2,
                'o3': forecast.current_aqi_o3,
                'so2': forecast.current_aqi_so2,
                'pm2_5': forecast.current_aqi_pm2_5,
                'pm10': forecast.current_aqi_pm10,
                'us-epa-index': forecast.current_aqi_us_epa_index,
            }
        },
        'hourly': [{
            'time': hour.time.strftime('%Y-%m-%d %H:%M'),
            'temp_c': hour.temp_c,
            'condition': hour.condition,
            'condition_icon': hour.condition_icon,
            'wind_kph': hour.wind_kph,
            'wind_dir': hour.wind_dir,
            'pressure_mb': hour.pressure_mb,
            'precip_mm': hour.precip_mm,
            'humidity': hour.humidity,
            'cloud': hour.cloud,
            'feelslike_c': hour.feelslike_c,
            'chance_of_rain': hour.chance_of_rain
        } for hour in hourly_data]
    }
    
    return JsonResponse(response_data)
