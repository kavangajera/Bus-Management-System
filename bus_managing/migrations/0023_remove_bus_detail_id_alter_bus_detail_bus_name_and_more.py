# Generated by Django 5.0.2 on 2024-03-30 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_managing', '0022_alter_bus_detail_id_alter_citiesorder_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bus_detail',
            name='id',
        ),
        migrations.AlterField(
            model_name='bus_detail',
            name='bus_name',
            field=models.CharField(max_length=122, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='citiesorder',
            name='time',
            field=models.TimeField(default='17:03'),
        ),
    ]
