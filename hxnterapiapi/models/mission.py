from django.db import models
from .hunter import Hunter
from .wanted import Wanted
from .type import Type


class Mission(models.Model):
    hunter = models.ForeignKey(Hunter, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    wanted = models.ForeignKey(Wanted, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
