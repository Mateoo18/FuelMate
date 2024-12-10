from django.db import models
from django.contrib.auth.models import User

class Points(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='ranking_points'  # Dodaj unikalną nazwę relacji
    )
    points = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed = False
        db_table = 'points'