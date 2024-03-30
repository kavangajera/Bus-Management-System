# Generated by Django 5.0.2 on 2024-03-05 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_managing', '0007_remove_route_detail_cities'),
    ]

    operations = [
        migrations.CreateModel(
            name='CitiesOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus_managing.city_detail')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus_managing.route_detail')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]