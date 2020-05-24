from django.test import TestCase

# Create your tests here.
from .models import Character

class CharacterModelTests(TestCase):

    def test_quoted_name(self):
        """
        quoted_name() correctly quotes the name of a character
        """
        testChar1 = Character(name='palutena/$.&', number=54, image='palutena.jpg')
        testChar2 = Character(name='Mr. Game & Watch', number=26, image='palutena.jpg')
        self.assertEqual(testChar1.quoted_name(), 'palutena%2F%24.%26')
        self.assertEqual(testChar2.quoted_name(), 'Mr.%20Game%20%26%20Watch')

    def test_image_link(self):
        """
        image_link() correctly appends the right path to the image (currently 'guide/images/')
        """
        testChar = Character(name='palutena', number=54, image='palutena.jpg')
        self.assertEqual(testChar.image_link(), 'guide/images/palutena.jpg')