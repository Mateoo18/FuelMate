# Generated by Django 5.1.3 on 2024-11-11 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_postal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='postal_code',
            field=models.CharField(max_length=6),
        ),
    ]