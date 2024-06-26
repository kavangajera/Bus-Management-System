# Generated by Django 5.0.2 on 2024-03-30 06:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_managing', '0017_remove_distance_id_distance_dis_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bus_detail',
            name='route_id',
        ),
        migrations.AlterField(
            model_name='citiesorder',
            name='time',
            field=models.TimeField(default='06:09'),
        ),
        migrations.AddField(
            model_name='bus_detail',
            name='route_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bus_managing.route_detail'),
        ),
    ]
