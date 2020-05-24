from django.test import TestCase

# Create your tests here.
from django.urls import reverse

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

class HomepageViewTests(TestCase):

    def test_no_characters(self):
        """
        If no characters exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('guide:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No characters at this time.")
        self.assertQuerysetEqual(response.context['character_list'], [])
    
    def test_one_character(self):
        """
        Check that homepage displays a character correctly
        """
        Character.objects.create(name='Palutena', number=54, image='palutena.jpg')
        response = self.client.get(reverse('guide:homepage'))
        self.assertQuerysetEqual(
            response.context['character_list'],
            ['<Character: Palutena>']
        )

    def test_multiple_characters(self):
        """
        Check that homepage displays multiple character correctly (in alphabetical order)
        """
        Character.objects.create(name='Mario', number=1, image='palutena.jpg')
        Character.objects.create(name='Palutena', number=54, image='palutena.jpg')
        Character.objects.create(name='Link', number=3, image='palutena.jpg')
        response = self.client.get(reverse('guide:homepage'))
        self.assertQuerysetEqual(
            response.context['character_list'],
            ['<Character: Link>', '<Character: Mario>', '<Character: Palutena>']
        )