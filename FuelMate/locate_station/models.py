# models.py
from django.db import models
from django.contrib.auth.models import User
from stations.models import Gas_Stations

class PostalCode(models.Model):
    zip_code = models.CharField(max_length=10, primary_key=True)  # Klucz główny
    country = models.CharField(max_length=100)
    place = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'postal_code'  # Nazwa tabeli w bazie danych
        managed = False  # Django nie zarządza tą tabelą
