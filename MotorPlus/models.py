from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, User
#from jsonfield import JSONField
# Create your models here.

class User(AbstractUser):
    isAdmin = models.BooleanField(default=False)

class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.IntegerField()
    vehicle_class = models.CharField(max_length=30)
    fuel_type = models.CharField(max_length=30)
    transmission = models.CharField(max_length=30)
    city_mpg = models.FloatField()
    highway_mpg = models.FloatField()
    displacement = models.FloatField()
    cylinders = models.FloatField()
    combination_mpg_api = models.DecimalField(max_digits=5, decimal_places=2)
    combination_mpg_predicted = models.DecimalField(max_digits=5, decimal_places=2)

class Profile(models.Model):
    # Add a relationship to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    motorcycles = models.ManyToManyField(Vehicle)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

class APIVehicle(models.Model):
    make = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    year = models.IntegerField()
    #APIInfo = JSONField()