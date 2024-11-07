# Generated by Django 5.1.2 on 2024-11-06 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_preference_max_temperature_alert_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preference',
            name='max_temperature_alert',
            field=models.FloatField(default=40, help_text='Set maximum temperature alert in Celsius.'),
        ),
        migrations.AlterField(
            model_name='preference',
            name='min_temperature_alert',
            field=models.FloatField(default=20, help_text='Set minimum temperature alert in Celsius.'),
        ),
    ]