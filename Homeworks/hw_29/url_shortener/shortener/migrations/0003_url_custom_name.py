# Generated by Django 5.1.4 on 2025-01-02 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0002_urlclick_country_urlclick_device_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='custom_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]