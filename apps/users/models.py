from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import MyAccountManager
import hashlib

class Account(AbstractBaseUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    gender = models.CharField(choices=GENDER_CHOICES, default='male', max_length=10)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def get_avatar(self):
        email = self.email
        email_hash = hashlib.md5(email.encode()).hexdigest()
        root_url = 'https://www.gravatar.com/avatar/'
        avatar = f"{root_url}{email_hash}"
        return avatar
    
    @property
    def get_name(self):
        return self.name if self.name else self.email.split('@')[0]
    
class Preference(models.Model):
    TEMPERATURE_UNITS = (
        ('C', 'Celsius'),
        ('F', 'Fahrenheit'),
    )
    ALERT_FREQUENCY = (
        ('immediately', 'Immediately'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    )
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    temperature_unit = models.CharField(max_length=1, choices=TEMPERATURE_UNITS)
    alert_frequency = models.CharField(max_length=15, choices=ALERT_FREQUENCY)
    
    def __str__(self):
        return f"{self.account.get_name}'s Preferences"

class Alert(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    min_temp_c = models.FloatField(default=20)
    max_temp_c = models.FloatField(default=40)
    rain_probability = models.FloatField(default=70)
    message = models.CharField(max_length=255, null=True, blank=True)
    is_shown = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message