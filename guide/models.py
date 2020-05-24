from django.db import models
import urllib.parse

# Create your models here.

class Character(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    number = models.IntegerField()
    image = models.CharField(max_length=30)

    def __str__(self):
        """
        String representation is the character name.
        """
        return self.name

    def quoted_name(self):
        """
        Returns the url safe version of character name.
        Django autoescapes html so seemingly pointless.
        """
        return urllib.parse.quote(self.name, safe='')

    def image_link(self):
        """
        Returns the path to the image of the character.
        """
        return 'guide/images/' + self.image