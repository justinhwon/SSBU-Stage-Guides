from django.db import models

# Create your models here.

class Character(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    number = models.IntegerField()
    image = models.CharField(max_length=30)