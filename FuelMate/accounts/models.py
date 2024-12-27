# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    fuel_type = models.CharField(max_length=50, default='Gaz')

    city = models.CharField(max_length=100)

    postal_code = models.CharField(max_length=6)



    def __str__(self):

        return self.user.username