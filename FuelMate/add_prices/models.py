from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Fuel(models.Model):
    Fuel_Id = models.BigAutoField(primary_key=True)
    Name = models.CharField(max_length=100)

    class Meta:
        managed = False
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
        managed = False
        db_table = 'Gas_Stations'


class StationFuel(models.Model):
    station = models.ForeignKey(Gas_Stations, db_column='Station_Id', on_delete=models.CASCADE)
    fuel = models.ForeignKey(Fuel, db_column='Fuel_Id', on_delete=models.CASCADE)
    Price = models.DecimalField(max_digits=5, decimal_places=2)
    Update_Date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Określenie, że Station_Fuel_Id to klucz główny
    Station_Fuel_Id = models.AutoField(primary_key=True)

    class Meta:
        managed = False  # Nie chcesz, aby Django zarządzało tabelą
        db_table = 'Station_Fuel'  # Określenie nazwy tabeli w bazie danych


class Points(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relacja do modelu User
    points = models.IntegerField()  # Liczba punktów
    date = models.DateTimeField(auto_now_add=True)  # Data dodania punktów


    class Meta:
        managed = False
        db_table = 'points'


class PriceHistory(models.Model):
    price_history_id = models.BigAutoField(db_column='Price_History_Id', primary_key=True)
    station = models.ForeignKey(Gas_Stations, db_column='id_stations', on_delete=models.SET_NULL, null=True)
    fuel = models.ForeignKey(Fuel, db_column='Fuel_Id', on_delete=models.SET_NULL, null=True)
    price = models.FloatField(db_column='Price')
    change_date = models.DateTimeField(db_column='Change_Date')

    class Meta:
        managed = False
        db_table = 'Price_History'

class Complain(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'Complain'