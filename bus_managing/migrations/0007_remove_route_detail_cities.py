# Generated by Django 5.0.2 on 2024-03-05 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bus_managing', '0006_alter_route_detail_cities'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route_detail',
            name='cities',
        ),
    ]
