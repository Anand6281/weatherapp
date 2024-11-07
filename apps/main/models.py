from django.db import models

class WeatherForecast(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location_name = models.CharField(max_length=100)  # Store the location name from API response
    date = models.DateField()
    last_updated = models.DateTimeField(auto_now=True)
    
    # Current weather
    current_temp_c = models.FloatField()
    current_condition = models.CharField(max_length=100)
    current_condition_icon = models.URLField()
    current_wind_kph = models.FloatField()
    current_wind_dir = models.CharField(max_length=5)
    current_pressure_mb = models.FloatField()
    current_precip_mm = models.FloatField()
    current_humidity = models.IntegerField()
    current_cloud = models.IntegerField()
    current_feelslike_c = models.FloatField()
    min_temp_c = models.FloatField(default=0)
    max_temp_c = models.FloatField(default=0)
    
    # Air Quality
    current_aqi_co = models.FloatField()
    current_aqi_no2 = models.FloatField()
    current_aqi_o3 = models.FloatField()
    current_aqi_so2 = models.FloatField()
    current_aqi_pm2_5 = models.FloatField()
    current_aqi_pm10 = models.FloatField()
    current_aqi_us_epa_index = models.IntegerField()
    
    class Meta:
        indexes = [
            models.Index(fields=['latitude', 'longitude', 'last_updated']),
        ]

class HourlyForecast(models.Model):
    weather_forecast = models.ForeignKey(WeatherForecast, related_name='hourly_forecasts', on_delete=models.CASCADE)
    time = models.DateTimeField()
    temp_c = models.FloatField()
    condition = models.CharField(max_length=100)
    condition_icon = models.URLField()
    wind_kph = models.FloatField()
    wind_dir = models.CharField(max_length=5)
    pressure_mb = models.FloatField()
    precip_mm = models.FloatField()
    humidity = models.IntegerField()
    cloud = models.IntegerField()
    feelslike_c = models.FloatField()
    chance_of_rain = models.IntegerField()
    
    class Meta:
        unique_together = ('weather_forecast', 'time')
        indexes = [
            models.Index(fields=['weather_forecast', 'time']),
        ]

