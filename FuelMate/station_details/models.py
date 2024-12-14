from django.db import models
from django.contrib.auth.models import User

class Gas_Stations(models.Model):
    id_stations = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    class Meta:
        db_table = 'Gas_Stations'

class StationRating(models.Model):
    id_stations = models.OneToOneField(
        Gas_Stations,
        on_delete=models.CASCADE,
        db_column='id_stations',
        related_name='rating',
        primary_key=True
    )
    rating = models.FloatField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'station_rating'