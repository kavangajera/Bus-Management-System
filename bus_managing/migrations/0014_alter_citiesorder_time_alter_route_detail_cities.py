# Generated by Django 5.0.2 on 2024-03-12 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_managing', '0013_alter_citiesorder_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citiesorder',
            name='time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='route_detail',
            name='cities',
            field=models.ManyToManyField(related_name='route_cities', through='bus_managing.CitiesOrder', to='bus_managing.city_detail'),
        ),
    ]
