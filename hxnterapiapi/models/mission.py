from django.db import models
from .hunter import Hunter
from .wanted import Wanted

TYPE_CHOICES = [
    ("capture", "Capture"),
    ("surveillance", "Surveillance"),
    ("investigation", "Investigation"),
]


class Mission(models.Model):
    hunter = models.ForeignKey(Hunter, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    wanted = models.ForeignKey(Wanted, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
