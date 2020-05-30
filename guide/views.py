from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic

import urllib.parse
from django.db.models import Avg
import math

from .models import Character

class HomepageView(generic.ListView):
    template_name = 'guide/homepage.html'
    context_object_name = 'character_list'

    def get_queryset(self):
        """
        Return all characters ordered alphabetically.
        """
        return Character.objects.order_by('name')


# helper function for CharacterView to map variable names to readable names
def varToName(d):
    mappedDict = []
    for key, value in d.items():
        img = ''
        # map to readable names
        if key == 'battlefield__avg':
            key = 'Battlefield'
            img = 'guide/stage_images/' + 'battlefield.png'
        elif key == 'final_destination__avg':
            key = 'Final Destination'
            img = 'guide/stage_images/' + 'final_destination.jpg'
        elif key == 'pokemon_stadium__avg':
            key = 'Pokémon Stadium 2'
            img = 'guide/stage_images/' + 'pokemon_stadium.png'
        elif key == 'smashville__avg':
            key = 'Smashville'
            img = 'guide/stage_images/' + 'smashville.png'
        elif key == 'lylat__avg':
            key = 'Lylat Cruise'
            img = 'guide/stage_images/' + 'lylat.jpg'
        elif key == 'town__avg':
            key = 'Town and City'
            img = 'guide/stage_images/' + 'town.png'
        elif key == 'kalos__avg':
            key = 'Kalos Pokémon League'
            img = 'guide/stage_images/' + 'kalos.png'
        elif key == 'yoshi_story__avg':
            key = "Yoshi's Story"
            img = 'guide/stage_images/' + 'yoshi_story.png'
        elif key == 'yoshi_island__avg':
            key = "Yoshi's Island"
            img = 'guide/stage_images/' + 'yoshi_island.png'
        elif key == 'unova__avg':
            key = "Unova Pokémon League"
            img = 'guide/stage_images/' + 'unova.png'
        temp = (key, value, img)
        mappedDict.append(temp)
    return mappedDict

class CharacterView(generic.DetailView):
    model = Character
    template_name = 'guide/character.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Process the votes into a list then add to context
        character = context['character']
        votes = character.vote_set.all()
        
        # if no votes, empty list
        if not votes:
            context['votes'] = []
            context['num_votes'] = 0
        # otherwise get average score and order list
        else:
            # get average score of each stage
            vote_avgs_dict = votes.aggregate(Avg('battlefield'), Avg('final_destination'), Avg('pokemon_stadium'),
                Avg('smashville'), Avg('town'), Avg('lylat'), Avg('kalos'), Avg('yoshi_story'), 
                Avg('yoshi_island'), Avg('unova'))

            # convert to list of form (stage_name, score)
            vote_avgs = varToName(vote_avgs_dict)

            # sort stage by avg score
            vote_avgs.sort(key = lambda x: -1 * math.inf if x[1] is None else x[1], reverse=True)

            # set context
            context['votes'] = vote_avgs
            context['num_votes'] = len(votes)
        return context

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