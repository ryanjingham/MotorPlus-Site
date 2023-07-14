from django.db import models
from django.conf import settings
# Create your models here.
class Vehicle(models.Model):
    
    ORIGIN_CHOICES = [
        ('USA', 'USA'),
        ('Europe', 'Europe'),
        ('Japan', 'Japan'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.IntegerField()
    name = models.CharField(max_length=30)
    is_custom = models.BooleanField(default=False)
    transmission = models.CharField(max_length=1)
    displacement = models.FloatField()
    cylinders = models.FloatField()
    horsepower = models.IntegerField()
    weight = models.IntegerField()
    acceleration = models.FloatField()
    origin = models.CharField(max_length=10, choices=ORIGIN_CHOICES)
    mpg_api = models.DecimalField(max_digits=5, decimal_places=2)
    mpg_predicted = models.DecimalField(max_digits=5, decimal_places=2)

class APIVehicle(models.Model):
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.IntegerField()
    #APIInfo = JSONField()
    
    
    