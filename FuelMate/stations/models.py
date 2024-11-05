from asyncio.windows_events import CONNECT_PIPE_MAX_DELAY

from django.db import models
from django.template.context_processors import request


class Fuel(models.Model):
    fuel_id = models.BigAutoField(db_column='Fuel_Id', primary_key=True)
    Name = models.CharField(db_column='Name', max_length=100)

    class Meta:
        managed=False
        db_table = 'Fuel'


class Gas_Stations(models.Model):
    Station_Id = models.BigAutoField(db_column='Station_Id', primary_key=True)
    Address = models.CharField(db_column='Address', max_length=100)
    City = models.CharField(db_column='City', max_length=100)
    Zip = models.CharField(db_column='Postal_Code', max_length=100)
    Name = models.CharField(db_column='Name', max_length=100)
    Latitude = models.FloatField(db_column='Latitude')
    Longitude = models.FloatField(db_column='Longitude')

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
    UserId = models.BigAutoField(db_column='User_Id', primary_key=True)
    First_name = models.CharField(db_column='First_Name', max_length=100)
    Last_name = models.CharField(db_column='Last_Name', max_length=100)
    Email = models.EmailField(db_column='Email_Address', max_length=100,unique=True)
    Password = models.CharField(db_column='Password', max_length=100)
    Address = models.CharField(db_column='City_of_Residence', max_length=100)
    Postal_Code = models.CharField(db_column='Postal_Code', max_length=100)
    Fuel = models.ForeignKey('Fuel', db_column='Fuel_Id',on_delete=models.SET_NULL,null = True)
    Role_Id = models.ForeignKey('Roles', db_column='Role_Id',on_delete=models.SET_NULL,null = True)

    class Meta:
        managed=False
        db_table = 'Users'


class Notifications(models.Model):
    Notification_Id = models.BigAutoField(db_column='Notification_Id', primary_key=True)
    User_Id = models.ForeignKey('Users', db_column='User_Id',on_delete=models.SET_NULL,null = True)
    Station_Id = models.ForeignKey('Gas_Stations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
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
    Station_Id = models.ForeignKey('Gas_Stations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
    Fuel_Id = models.ForeignKey('Fuel', db_column='Fuel_Id',on_delete=models.SET_NULL,null = True)
    Reported_price = models.FloatField(db_column='Reported_Price')
    Reported_date = models.DateTimeField(db_column='Report_Date')
    Comment = models.CharField(db_column='Comment', max_length=100)

    class Meta:
        managed=False
        db_table = 'Reports'


class Station_Rev(models.Model):
    Station_Reviews_Id = models.BigAutoField(db_column='Station_Reviews_Id', primary_key=True)
    Station_Id = models.ForeignKey('Gas_Stations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
    User_Id = models.ForeignKey('Users', db_column='User_Id',on_delete=models.SET_NULL,null = True)
    Rating = models.FloatField(db_column='Rating')
    Comment = models.CharField(db_column='Comment', max_length=100)
    Date = models.DateTimeField(db_column='Review_Date')

    class Meta:
        managed=False
        db_table = 'Station_Reviews'

class Promotion(models.Model):
    Promotion_Id = models.BigAutoField(db_column='Promotions_Id', primary_key=True)
    Station_Id = models.ForeignKey('Gas_Stations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
    User_Id = models.ForeignKey('Users', db_column='User_Id',on_delete=models.SET_NULL,null = True)
    Fuel_Id = models.ForeignKey('Fuel', db_column='Fuel_Id',on_delete=models.SET_NULL,null = True)
    Start_Date = models.DateTimeField(db_column='Start_Date')
    End_Date = models.DateTimeField(db_column='End_Date')
    Comment = models.CharField(db_column='Promotion_Description', max_length=100)

    class Meta:
        managed=False
        db_table = 'Promotions'

class Favorite_Station(models.Model):
    Favorite_Id = models.BigAutoField(db_column='Favorite_Stations_Id', primary_key=True)
    User_Id = models.ForeignKey('Users', db_column='User_Id',on_delete=models.SET_NULL,null = True)
    Station_Id = models.ForeignKey('Gas_Stations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)

    class Meta:
        managed=False
        db_table = 'Favorite_Stations'

class Price_history(models.Model):
    Price_Id = models.BigAutoField(db_column='Price_History_Id', primary_key=True)
    Station_Id = models.ForeignKey('Gas_Stations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
    Fuel_Id = models.ForeignKey('Fuel', db_column='Fuel_Id',on_delete=models.SET_NULL,null = True)
    Price = models.FloatField(db_column='Price')
    Date = models.DateTimeField(db_column='Change_Date')

    class Meta:
        managed=False
        db_table = 'Price_History'

class Station_Fuel(models.Model):
    Station_Fuel_Id = models.BigAutoField(db_column='Station_Fuel_Id', primary_key=True)
    Station_Id = models.ForeignKey('Gas_Stations', db_column='Station_Id',on_delete=models.SET_NULL,null = True)
    Fuel_Id = models.ForeignKey('Fuel', db_column='Fuel_Id',on_delete=models.SET_NULL,null = True)
    Price = models.FloatField(db_column='Price')
    Date = models.DateTimeField(db_column='Update_Date')

    class Meta:
        managed=False
        db_table = 'Station_Fuel'