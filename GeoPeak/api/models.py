from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Peak(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    lat = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    long = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    altitude = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.name} ({self.altitude} mètres)"
