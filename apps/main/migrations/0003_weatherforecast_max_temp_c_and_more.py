# Generated by Django 5.1.2 on 2024-11-06 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_weatherforecast_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='weatherforecast',
            name='max_temp_c',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='weatherforecast',
            name='min_temp_c',
            field=models.FloatField(default=0),
        ),
    ]