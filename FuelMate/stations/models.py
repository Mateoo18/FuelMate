from django.db import models

class Fuel(models.Model):
    Fuel_Id = models.AutoField(primary_key=True)  # Primary key
    Name = models.CharField(max_length=100)       # Name column

    class Meta:
        db_table = 'Fuel'

    def __str__(self):
        return self.Name

