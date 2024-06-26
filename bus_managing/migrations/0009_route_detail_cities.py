# Generated by Django 5.0.2 on 2024-03-05 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_managing', '0008_citiesorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='route_detail',
            name='cities',
            field=models.ManyToManyField(limit_choices_to={'city__in': ['Junagadh', 'Rajkot', 'Nadiad']}, related_name='route_cities', through='bus_managing.CitiesOrder', to='bus_managing.city_detail'),
        ),
    ]
