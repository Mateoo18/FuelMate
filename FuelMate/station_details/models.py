from django.db import models
from django.contrib.auth.models import User



class StationRating(models.Model):
    id_stations = models.ForeignKey('stations.Gas_Stations', on_delete=models.CASCADE)
    rating = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'station_rating'