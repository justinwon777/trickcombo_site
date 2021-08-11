from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TrickSet(models.Model):
    name = models.CharField(max_length=120)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tricks = models.JSONField()

    def __str__(self):
        return self.name


class Combo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    combo_name = models.CharField(max_length=300)


class Trick(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    trick_name = models.CharField(max_length=100)
