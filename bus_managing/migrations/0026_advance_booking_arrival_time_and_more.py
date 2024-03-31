# Generated by Django 5.0.2 on 2024-03-31 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_managing', '0025_alter_citiesorder_time_bus_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='advance_booking',
            name='arrival_time',
            field=models.CharField(default=0, max_length=122),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='advance_booking',
            name='bus_info',
            field=models.CharField(default=0, max_length=122),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='advance_booking',
            name='departure_time',
            field=models.CharField(default=0, max_length=122),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='advance_booking',
            name='seat_nos',
            field=models.CharField(default=0, max_length=122),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='citiesorder',
            name='time',
            field=models.TimeField(default='08:44'),
        ),
    ]