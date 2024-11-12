from django.db import models
from django.template.context_processors import request
class Fuel(models.Model):
    fuel_id = models.BigAutoField(db_column='Fuel_Id', primary_key=True)
    Name = models.CharField(db_column='Name', max_length=100)

    class Meta:
        managed=False
        db_table = 'Fuel'


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
        managed=False
        db_table = 'Gas_Stations'


class Station_Fuel(models.Model):
    Station_Fuel_Id = models.BigAutoField(db_column='Station_Fuel_Id', primary_key=True)
    Station_Id = models.ForeignKey('Gas_Stations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
    Fuel_Id = models.ForeignKey('Fuel', db_column='Fuel_Id',on_delete=models.SET_NULL,null = True)
    Price = models.FloatField(db_column='Price')
    Date = models.DateTimeField(db_column='Update_Date')

    class Meta:
        managed=False
        db_table = 'Station_Fuel'

class Price_history(models.Model):
    Price_Id = models.BigAutoField(db_column='Price_History_Id', primary_key=True)
    Station_Id = models.ForeignKey('Gas_Stations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
    Fuel_Id = models.ForeignKey('Fuel', db_column='Fuel_Id',on_delete=models.SET_NULL,null = True)
    Price = models.FloatField(db_column='Price')
    Date = models.DateTimeField(db_column='Change_Date')

    class Meta:
        managed=False
        db_table = 'Price_History'