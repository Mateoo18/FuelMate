# Generated by Django 5.1.2 on 2024-11-04 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0002_alter_fuel_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fuel',
            old_name='Fuel_ID',
            new_name='Fuel_Id',
        ),
    ]