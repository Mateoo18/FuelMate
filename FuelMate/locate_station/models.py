# models.py
from django.db import models
from django.contrib.auth.models import User

class GasStation(models.Model):
    id_stations = models.AutoField(primary_key=True)  # Klucz główny
    name = models.CharField(max_length=255)
    address = models.TextField()
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'Gas_Stations'  # Nazwa tabeli w bazie danych
        managed = False  # Django nie zarządza tą tabelą


class PostalCode(models.Model):
    zip_code = models.CharField(max_length=10, primary_key=True)  # Klucz główny
    country = models.CharField(max_length=100)
    place = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'postal_code'  # Nazwa tabeli w bazie danych
        managed = False  # Django nie zarządza tą tabelą
