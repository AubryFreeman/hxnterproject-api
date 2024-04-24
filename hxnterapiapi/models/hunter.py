from django.db import models
from django.contrib.auth.models import User


class Hunter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_pic = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    bio = models.TextField()
    specialization = models.CharField(max_length=100)
