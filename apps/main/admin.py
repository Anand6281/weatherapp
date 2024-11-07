from django.contrib import admin
from django.utils.html import format_html
from apps.main.models import WeatherForecast, HourlyForecast

# Register your models here.
class HourlyForecastInline(admin.TabularInline):
    model = HourlyForecast
    extra = 0
    readonly_fields = [
        'time', 'temp_c', 'condition', 'condition_icon_display',
        'wind_kph', 'wind_dir', 'pressure_mb', 'precip_mm',
        'humidity', 'cloud', 'feelslike_c', 'chance_of_rain'
    ]
    fields = readonly_fields
    can_delete = False
    max_num = 0
    
    def condition_icon_display(self, obj):
        if obj.condition_icon:
            return format_html('<img src="{}" height="30" />', obj.condition_icon)
        return ""
    condition_icon_display.short_description = "Condition Icon"

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = [
        'location_name', 
        'latitude', 
        'longitude', 
        'date', 
        'current_temp_c',
        'current_condition',
        'current_humidity',
        'last_updated'
    ]
    
    list_filter = [
        'location_name',
        'date',
        'last_updated',
        'current_condition',
    ]
    
    search_fields = [
        'location_name',
        'latitude',
        'longitude',
        'current_condition',
    ]
    
    readonly_fields = [
        'location_name',
        'latitude',
        'longitude',
        'date',
        'last_updated',
        'current_temp_c',
        'current_condition',
        'current_condition_icon_display',
        'current_wind_kph',
        'current_wind_dir',
        'current_pressure_mb',
        'current_precip_mm',
        'current_humidity',
        'current_cloud',
        'current_feelslike_c',
        'current_aqi_co',
        'current_aqi_no2',
        'current_aqi_o3',
        'current_aqi_so2',
        'current_aqi_pm2_5',
        'current_aqi_pm10',
        'current_aqi_us_epa_index',
    ]

    fieldsets = (
        ('Location Information', {
            'fields': (
                'location_name',
                ('latitude', 'longitude'),
                'date',
                'last_updated',
            )
        }),
        ('Current Weather', {
            'fields': (
                ('current_temp_c', 'current_feelslike_c'),
                ('min_temp_c', 'max_temp_c'),
                'current_condition',
                'current_condition_icon_display',
                ('current_wind_kph', 'current_wind_dir'),
                ('current_pressure_mb', 'current_precip_mm'),
                ('current_humidity', 'current_cloud'),
            )
        }),
        ('Air Quality Index', {
            'fields': (
                ('current_aqi_co', 'current_aqi_no2'),
                ('current_aqi_o3', 'current_aqi_so2'),
                ('current_aqi_pm2_5', 'current_aqi_pm10'),
                'current_aqi_us_epa_index',
            ),
            'classes': ('collapse',)
        }),
    )

    inlines = [HourlyForecastInline]

    def current_condition_icon_display(self, obj):
        if obj.current_condition_icon:
            return format_html('<img src="{}" height="30" />', obj.current_condition_icon)
        return ""
    current_condition_icon_display.short_description = "Current Condition Icon"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

@admin.register(HourlyForecast)
class HourlyForecastAdmin(admin.ModelAdmin):
    list_display = [
        'weather_forecast',
        'time',
        'temp_c',
        'condition',
        'wind_kph',
        'humidity',
        'chance_of_rain'
    ]
    
    list_filter = [
        'weather_forecast__location_name',
        'time',
        'condition',
    ]
    
    search_fields = [
        'weather_forecast__location_name',
        'condition',
    ]
    
    readonly_fields = [
        'weather_forecast',
        'time',
        'temp_c',
        'condition',
        'condition_icon_display',
        'wind_kph',
        'wind_dir',
        'pressure_mb',
        'precip_mm',
        'humidity',
        'cloud',
        'feelslike_c',
        'chance_of_rain'
    ]

    fieldsets = (
        (None, {
            'fields': (
                'weather_forecast',
                'time',
                ('temp_c', 'feelslike_c'),
                'condition',
                'condition_icon_display',
                ('wind_kph', 'wind_dir'),
                ('pressure_mb', 'precip_mm'),
                ('humidity', 'cloud'),
                'chance_of_rain',
            )
        }),
    )

    def condition_icon_display(self, obj):
        if obj.condition_icon:
            return format_html('<img src="{}" height="30" />', obj.condition_icon)
        return ""
    condition_icon_display.short_description = "Condition Icon"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
