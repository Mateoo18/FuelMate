from django.db import models

class GasStations(models.Model):
    Station_Id = models.BigAutoField(db_column='id_stations', primary_key=True)
    Address = models.CharField(db_column='address', max_length=100)
    City = models.CharField(db_column='city', max_length=100)
    Zip = models.CharField(db_column='postal_code', max_length=100)
    Name = models.CharField(db_column='name', max_length=100)
    Latitude = models.FloatField(db_column='latitude')
    Longitude = models.FloatField(db_column='longitude')
    Phone = models.CharField(db_column='phone', max_length=100)


    class Meta:
        managed=False
        db_table = 'Gas_Stations'

#
# class Station_Fuel (models.Model):
#     Station_Id = models.BigAutoField(db_column='Station_Id', primary_key=True)
#     Fuel_Id = models.BigAutoField(db_column='Fuel_Id', primary_key=True)
#     Price = models.FloatField(db_column='Price')
#     Update = models.CharField(db_column='Update_Date', max_length=100)
#     Station_Fuel_Id = models.FloatField(db_column='Price')
#     user_id = models.FloatField(db_column='Price')