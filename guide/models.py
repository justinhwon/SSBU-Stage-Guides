from django.db import models
import urllib.parse

# Create your models here.

class Character(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    number = models.IntegerField()
    image = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def quoted_name(self):
        return urllib.parse.quote(self.name, safe='')

    def image_link(self):
        return 'guide/images/' + self.image