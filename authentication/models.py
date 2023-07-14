from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, User
# Create your models here.

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location=models.CharField(max_length=30, blank=True)
    API_KEY=models.CharField(max_length=255, blank=True)
    
    
    