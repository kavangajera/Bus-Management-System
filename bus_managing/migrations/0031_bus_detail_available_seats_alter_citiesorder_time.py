# Generated by Django 5.0.2 on 2024-04-02 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_managing', '0030_advance_booking_doj_alter_citiesorder_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus_detail',
            name='available_seats',
            field=models.IntegerField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='citiesorder',
            name='time',
            field=models.TimeField(default='04:28'),
        ),
    ]
