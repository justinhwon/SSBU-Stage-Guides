from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic

import urllib.parse

from .models import Character

class HomepageView(generic.ListView):
    template_name = 'guide/homepage.html'
    context_object_name = 'character_list'

    def get_queryset(self):
        """
        Return all characters ordered alphabetically.
        """
        return Character.objects.order_by('name')

class CharacterView(generic.DetailView):
    model = Character
    template_name = 'guide/character.html'

class ContactView(generic.TemplateView):
    template_name = 'guide/contact.html'

class MatchupsView(generic.ListView):
    template_name = 'guide/matchups.html'
    context_object_name = 'character_list'

    def get_queryset(self):
        """
        Return all characters ordered alphabetically.
        """
        return Character.objects.order_by('name')