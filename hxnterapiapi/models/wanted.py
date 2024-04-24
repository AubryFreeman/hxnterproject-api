from django.db import models
from django.contrib.auth.models import User


class Wanted(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    description = models.TextField()
    wanted_for = models.CharField(max_length=200)
