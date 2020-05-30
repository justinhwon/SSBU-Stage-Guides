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

class Vote(models.Model):
    # name of character is foreign key
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    # the name of stage represents the vote value
    battlefield = models.SmallIntegerField(blank=True, null=True)
    final_destination = models.SmallIntegerField(blank=True, null=True)
    pokemon_stadium = models.SmallIntegerField(blank=True, null=True)
    smashville = models.SmallIntegerField(blank=True, null=True)
    town = models.SmallIntegerField(blank=True, null=True)
    lylat = models.SmallIntegerField(blank=True, null=True)
    kalos = models.SmallIntegerField(blank=True, null=True)
    yoshi_story = models.SmallIntegerField(blank=True, null=True)
    yoshi_island = models.SmallIntegerField(blank=True, null=True)
    unova = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        """
        String representation is the character name.
        """
        return (str(self.character) + str(self.battlefield) + str(self.final_destination) + str(self.pokemon_stadium) + 
                str(self.smashville) + str(self.town) + str(self.lylat) + str(self.kalos) + str(self.yoshi_story) + 
                str(self.yoshi_island) + str(self.unova) )