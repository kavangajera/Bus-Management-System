# Generated by Django 5.0.2 on 2024-03-31 07:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_managing', '0024_bus_detail_bus_id_alter_bus_detail_bus_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citiesorder',
            name='time',
            field=models.TimeField(default='07:57'),
        ),
        migrations.CreateModel(
            name='Bus_Seats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_no', models.CharField(max_length=122)),
                ('bus_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bus_managing.bus_detail')),
            ],
        ),
    ]
