from django.contrib import admin
from .models import *

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):          
    list_display = ('name', 'email', 'gender', 'created_at',)
    search_fields = ('name', 'email',)
    list_filter = ('gender',)
    
@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ('account', 'alert_frequency',)
    search_fields = ('account',)
    
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('account', 'message', 'is_shown', 'created_at',)
    search_fields = ('account', 'message',)
    list_filter = ('is_shown',)