# Generated by Django 5.1.2 on 2024-11-07 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_preference_max_temperature_alert_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='message',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='rain_probability',
            field=models.FloatField(default=70, help_text='Set rain probability in percentage.'),
        ),
    ]
