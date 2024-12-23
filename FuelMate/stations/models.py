from django.db import models
from django.contrib.auth.models import User
class Fuel(models.Model):
    fuel_id = models.BigAutoField(db_column='Fuel_Id', primary_key=True)
    Name = models.CharField(db_column='Name', max_length=100)

    class Meta:
        managed=False
        db_table = 'Fuel'


class GasStations(models.Model):
    Station_Id = models.BigAutoField(db_column='id_stations', primary_key=True)
    Address = models.CharField(db_column='address', max_length=100)
    City = models.CharField(db_column='city', max_length=100)
    postal_code = models.CharField(db_column='postal_code', max_length=100)
    Name = models.CharField(db_column='name', max_length=100)
    Latitude = models.FloatField(db_column='latitude')
    Longitude = models.FloatField(db_column='longitude')
    Phone = models.CharField(db_column='phone', max_length=100)


    class Meta:
        managed=False
        db_table = 'Gas_Stations'





class Roles(models.Model):
    Role_Id = models.BigAutoField(db_column='Role_Id', primary_key=True)
    Role_Name = models.CharField(db_column='Role_Name', max_length=100)

    class Meta:
        managed=False
        db_table = 'Roles'

class Users(models.Model):
    UserId = models.BigAutoField(db_column='id', primary_key=True)
    Last_login = models.DateTimeField(db_column='last_login', blank=True, null=True)
    Is_super_user = models.BooleanField(db_column='is_superuser')
    Username = models.CharField(db_column='username', max_length=100)
    First_name = models.CharField(db_column='first_name', max_length=100)
    Last_name = models.CharField(db_column='last_name', max_length=100)
    Email = models.EmailField(db_column='email', max_length=100,unique=True)
    Is_staff = models.BooleanField(db_column='is_staff')
    Is_active = models.BooleanField(db_column='is_active')
    Date_joined = models.DateTimeField(db_column='date_joined')

    class Meta:
        managed=False
        db_table = 'auth_user'


class FavoriteStation(models.Model):
    Favorite_Id = models.BigAutoField(db_column='Favorite_Stations_Id', primary_key=True)
    User_Id = models.ForeignKey('Users', db_column='User_Id',on_delete=models.SET_NULL,null = True)
    Station_Id = models.ForeignKey('GasStations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)

    class Meta:
        managed=False
        db_table = 'Favorite_Stations'


class Notifications(models.Model):
    Notification_Id = models.BigAutoField(db_column='Notification_Id', primary_key=True)
    User_Id = models.ForeignKey('Users', db_column='User_Id',on_delete=models.SET_NULL,null = True)
    Station_Id = models.ForeignKey('GasStations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
    Fuel_Id = models.ForeignKey('Fuel', db_column='Fuel_Id',on_delete=models.SET_NULL,null = True)
    Price_Threshold = models.FloatField(db_column='Price_Threshold')
    Status = models.CharField(db_column='Status', max_length=100)
    Setting_Date = models.DateTimeField(db_column='Setting_Date')


    class Meta:
        managed=False
        db_table = 'Notifications'

class Report(models.Model):
    Report_Id = models.BigAutoField(db_column='Reports_Id', primary_key=True)
    User_Id = models.ForeignKey('Users', db_column='User_Id',on_delete=models.SET_NULL,null = True)
    Station_Id = models.ForeignKey('GasStations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
    Fuel_Id = models.ForeignKey('Fuel', db_column='Fuel_Id',on_delete=models.SET_NULL,null = True)
    Reported_price = models.FloatField(db_column='Reported_Price')
    Reported_date = models.DateTimeField(db_column='Report_Date')
    Comment = models.CharField(db_column='Comment', max_length=100)

    class Meta:
        managed=False
        db_table = 'Reports'

class StationRev(models.Model):
    Station_Reviews_Id = models.BigAutoField(db_column='Station_Reviews_Id', primary_key=True)
    Station_Id = models.ForeignKey('GasStations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
    User_Id = models.ForeignKey('Users', db_column='User_Id',on_delete=models.SET_NULL,null = True)
    Rating = models.FloatField(db_column='Rating')
    Comment = models.CharField(db_column='Comment', max_length=100)
    Date = models.DateTimeField(db_column='Review_Date')

    class Meta:
        managed=False
        db_table = 'Station_Reviews'

class Promotion(models.Model):
    Promotion_Id = models.BigAutoField(db_column='Promotions_Id', primary_key=True)
    Station_Id = models.ForeignKey('GasStations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
    User_Id = models.ForeignKey('Users', db_column='User_Id',on_delete=models.SET_NULL,null = True)
    Fuel_Id = models.ForeignKey('Fuel', db_column='Fuel_Id',on_delete=models.SET_NULL,null = True)
    Start_Date = models.DateTimeField(db_column='Start_Date')
    End_Date = models.DateTimeField(db_column='End_Date')
    Comment = models.CharField(db_column='Promotion_Description', max_length=100)

    class Meta:
        managed=False
        db_table = 'Promotions'



class PriceHistory(models.Model):
    Price_Id = models.BigAutoField(db_column='Price_History_Id', primary_key=True)
    Station_Id = models.ForeignKey('GasStations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
    Fuel_Id = models.ForeignKey('Fuel', db_column='Fuel_Id',on_delete=models.SET_NULL,null = True)
    Price = models.FloatField(db_column='Price')
    Date = models.DateTimeField(db_column='Change_Date')

    class Meta:
        managed=False
        db_table = 'Price_History'

class StationFuel(models.Model):
    Station_Fuel_Id = models.BigAutoField(db_column='Station_Fuel_Id', primary_key=True)
    Station_Id = models.ForeignKey('GasStations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
    Fuel_Id = models.ForeignKey('Fuel', db_column='Fuel_Id',on_delete=models.SET_NULL,null = True)
    Price = models.FloatField(db_column='Price')
    Date = models.DateTimeField(db_column='Update_Date')

    class Meta:
        managed=False
        db_table = 'Station_Fuel'


class StationRating(models.Model):
    id_stations = models.OneToOneField(
        GasStations,
        on_delete=models.CASCADE,
        db_column='id_stations',
        related_name='rating',
        primary_key=True
    )
    rating = models.FloatField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'station_rating'

class PostalCode(models.Model):
    zip_code = models.CharField(max_length=10, primary_key=True)  # Klucz główny
    country = models.CharField(max_length=100)
    place = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = 'postal_code'  # Nazwa tabeli w bazie danych
        managed = False  # Django nie zarządza tą tabelą


class Complain(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    station = models.ForeignKey('GasStations',db_column='id_stations', on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'complain'


class Points(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relacja do modelu User
    points = models.IntegerField()  # Liczba punktów
    date = models.DateTimeField(auto_now_add=True)  # Data dodania punktów


    class Meta:
        managed = False
        db_table = 'points'

class RecommendStations(models.Model):
    remomendet_id = models.BigAutoField(primary_key=True)
    station_id =  models.ForeignKey('GasStations',db_column='station_id', on_delete=models.CASCADE)\

    class Meta:
        managed = False
        db_table = 'remomendet_stations'


