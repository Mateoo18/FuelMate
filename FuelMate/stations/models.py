from django.db import models

class Fuel(models.Model):
    fuel_id = models.BigAutoField(db_column='Fuel_Id', primary_key=True)
    Name = models.CharField(db_column='Name', max_length=100)

    class Meta:
        managed=False
        db_table = 'Fuel'

    def __str__(self):
        return self.fuel_id
        return self.Name

