from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.template import loader
from django.views import generic
from django import forms

import urllib.parse
from django.db.models import Avg
import math

from .models import Character, Vote

# the homepage
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
        temp = [key, value, img]
        mappedDict.append(temp)
    return mappedDict

# displays stage rankings for a character
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
            #vote_avgs.sort(key = lambda x: x[1], reverse=True)
            vote_avgs.sort(key = lambda x: -1 * math.inf if x[1] is None else x[1], reverse=True)

            # considered changing Nones to 0s, changed mind
            """
            # convert Nones to 0's
            for x in vote_avgs:
                if x[1] is None:
                    x[1] = 0
            """

            
            # set context
            context['votes'] = vote_avgs
            context['num_votes'] = len(votes)
        return context

# static page - contact information
class ContactView(generic.TemplateView):
    template_name = 'guide/contact.html'

# static page - info about the site
class AboutView(generic.TemplateView):
    template_name = 'guide/about.html'

# search page/form for matchups
class MatchupsView(generic.TemplateView):
    template_name = 'guide/matchups.html'

class VoteModelForm(forms.ModelForm):
    VOTEVALUES=[
         (3, '3: Best'),
         (2, '2: Great'),
         (1, '1: Good'),
         (0, '0: Neutral'),
         (-1, '-1: Bad'),
         (-2, '-2: Terrible'),
         (-3, '-3: Worst'),
         ('', 'N/A')
         ]
    
    battlefield = forms.ChoiceField(choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    final_destination = forms.ChoiceField(label='Final Destination', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    pokemon_stadium = forms.ChoiceField(label='Pokémon Stadium 2', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    smashville = forms.ChoiceField(choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    town = forms.ChoiceField(label='Town and City', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    lylat = forms.ChoiceField(label='Lylat Cruise', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    kalos = forms.ChoiceField(label='Kalos Pokémon League', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    yoshi_story = forms.ChoiceField(label="Yoshi's Story", choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    yoshi_island = forms.ChoiceField(label="Yoshi's Island", choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    unova = forms.ChoiceField(label='Unova Pokémon League', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    

    # make sure scores are between -2 and 2, and that blank strings convert to None
    def clean_battlefield(self):
        battlefield = self.cleaned_data['battlefield']
        if not battlefield:
            battlefield = None
        elif int(battlefield) > 3 or int(battlefield) < -3:
            raise forms.ValidationError("Only scores between -3 and 3 allowed.")
        return battlefield

    def clean_final_destination(self):
        final_destination = self.cleaned_data['final_destination']
        if not final_destination:
            final_destination = None
        elif int(final_destination) > 3 or int(final_destination) < -3:
            raise forms.ValidationError("Only scores between -3 and 3 allowed.")
        return final_destination
    
    def clean_pokemon_stadium(self):
        pokemon_stadium = self.cleaned_data['pokemon_stadium']
        if not pokemon_stadium:
            pokemon_stadium = None
        elif int(pokemon_stadium) > 3 or int(pokemon_stadium) < -3:
            raise forms.ValidationError("Only scores between -3 and 3 allowed.")
        return pokemon_stadium

    def clean_smashville(self):
        smashville = self.cleaned_data['smashville']
        if not smashville:
            smashville = None
        elif int(smashville) > 3 or int(smashville) < -3:
            raise forms.ValidationError("Only scores between -3 and 3 allowed.")
        return smashville
    
    def clean_town(self):
        town = self.cleaned_data['town']
        if not town:
            town = None
        elif int(town) > 3 or int(town) < -3:
            raise forms.ValidationError("Only scores between -3 and 3 allowed.")
        return town

    def clean_lylat(self):
        lylat = self.cleaned_data['lylat']
        if not lylat:
            lylat = None
        elif int(lylat) > 3 or int(lylat) < -3:
            raise forms.ValidationError("Only scores between -3 and 3 allowed.")
        return lylat

    def clean_kalos(self):
        kalos = self.cleaned_data['kalos']
        if not kalos:
            kalos = None
        elif int(kalos) > 3 or int(kalos) < -3:
            raise forms.ValidationError("Only scores between -3 and 3 allowed.")
        return kalos

    def clean_yoshi_story(self):
        yoshi_story = self.cleaned_data['yoshi_story']
        if not yoshi_story:
            yoshi_story = None
        elif int(yoshi_story) > 3 or int(yoshi_story) < -3:
            raise forms.ValidationError("Only scores between -3 and 3 allowed.")
        return yoshi_story

    def clean_yoshi_island(self):
        yoshi_island = self.cleaned_data['yoshi_island']
        if not yoshi_island:
            yoshi_island = None
        elif int(yoshi_island) > 3 or int(yoshi_island) < -3:
            raise forms.ValidationError("Only scores between -3 and 3 allowed.")
        return yoshi_island

    def clean_unova(self):
        unova = self.cleaned_data['unova']
        if not unova:
            unova = None
        elif int(unova) > 3 or int(unova) < -3:
            raise forms.ValidationError("Only scores between -3 and 3 allowed.")
        return unova

    class Meta:
        model = Vote
        fields = ['character', 'battlefield', 'final_destination', 'pokemon_stadium', 'smashville',
        'town', 'lylat', 'kalos', 'yoshi_story', 'yoshi_island', 'unova']
        widgets = {'character': forms.HiddenInput()}


class VoteView(generic.CreateView):
    template_name = 'guide/vote.html'
    form_class = VoteModelForm
    #success_url = reverse('guide:character')

    def get_success_url(self, **kwargs):
        return reverse('guide:character', args=[self.kwargs['charactername']])

    def get_initial(self, *args, **kwargs):
        initial = super(VoteView, self).get_initial(**kwargs)
        initial['character'] = self.kwargs['charactername']
        return initial

    def get_context_data(self, **kwargs):
        context = super(VoteView, self).get_context_data(**kwargs)
        context['character'] = get_object_or_404(Character, pk=self.kwargs['charactername'])
        return context

# redirects to character view using searchform info
def SearchView(request):
    try:
        characterObject = Character.objects.get(pk=request.GET['Character'])
    except (KeyError, Character.DoesNotExist):
        # Redisplay the question voting form.
        raise Http404("Character name does not exist. Please choose a name from the dropdown.")
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('guide:character', args=(request.GET['Character'],)))

# used by form from matchups search to redirect to matchup page
def MatchupSearchView(request):
    try:
        yourCharObject = Character.objects.get(pk=request.GET['Your Character'])
        oppCharObject = Character.objects.get(pk=request.GET['Opponent Character'])
    except (KeyError, Character.DoesNotExist):
        # Redisplay the question voting form.
        raise Http404("Character name does not exist. Please choose a name from the dropdown.")
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('guide:matchupinfo', args=(request.GET['Your Character'], request.GET['Opponent Character'])))

# displays the actual matchup info
class MatchupInfoView(generic.DetailView):
    model = Character
    template_name = 'guide/matchupinfo.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # add opponent character to context
        context['opponentChar'] = get_object_or_404(Character, pk=self.kwargs['opponentChar'])

        # Process the votes for player character into a list then add to context
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
            #vote_avgs.sort(key = lambda x: x[1], reverse=True)
            vote_avgs.sort(key = lambda x: -1 * math.inf if x[1] is None else x[1], reverse=True)

            # considered changing Nones to 0s, changed mind
            """
            # convert Nones to 0's
            for x in vote_avgs:
                if x[1] is None:
                    x[1] = 0
            """

            
            # set context
            context['votes'] = vote_avgs
            context['num_votes'] = len(votes)

        # Process the votes for opponent character into a list then add to context
        opponent = context['opponentChar']
        opp_votes = opponent.vote_set.all()
        
        # if no votes, empty list
        if not opp_votes:
            context['opp_votes'] = []
            context['num_opp_votes'] = 0
        # otherwise get average score and order list
        else:
            # get average score of each stage
            opp_vote_avgs_dict = opp_votes.aggregate(Avg('battlefield'), Avg('final_destination'), Avg('pokemon_stadium'),
                Avg('smashville'), Avg('town'), Avg('lylat'), Avg('kalos'), Avg('yoshi_story'), 
                Avg('yoshi_island'), Avg('unova'))

            # convert to list of form (stage_name, score)
            opp_vote_avgs = varToName(opp_vote_avgs_dict)

            # sort stage by avg score
            #vote_avgs.sort(key = lambda x: x[1], reverse=True)
            opp_vote_avgs.sort(key = lambda x: -1 * math.inf if x[1] is None else x[1], reverse=True)

            # considered changing Nones to 0s, changed mind
            """
            # convert Nones to 0's
            for x in vote_avgs:
                if x[1] is None:
                    x[1] = 0
            """

            
            # set context
            context['opp_votes'] = opp_vote_avgs
            context['num_opp_votes'] = len(opp_votes)

        # get the score differences between each characters rankings (from player char's POV)
        # if one of the characters has no votes, say not enough data
        if not context['votes'] or not context['opp_votes']:
            context['matchupscores'] = []
        # otherwise get score differentials by sorting by stagename and taking differences
        else:
            # sort vote avgs by stage name
            nameSortedVotes = sorted(vote_avgs, key=lambda x: x[0])
            nameSortedOppVotes = sorted(opp_vote_avgs, key=lambda x: x[0])
            #context['namevotes'] = nameSortedVotes
            #context['oppnamevotes'] = nameSortedOppVotes

            # for loop to get score differentials and individual scores for each stage
            matchup_scores = []
            for vote, oppvote in zip(nameSortedVotes, nameSortedOppVotes):
                score = vote[1]
                opp_score = oppvote[1]
                stage_name = vote[0]
                stage_img = vote[2]

                # need to check for empty values
                if score and opp_score:
                    score_diff = score - opp_score
                elif score is None and opp_score is None:
                    score_diff = None
                elif opp_score is None:
                    score_diff = score
                else: # no score
                    score_diff = -opp_score
                    
                matchup_scores.append([score, opp_score, stage_name, stage_img, score_diff])

            # sort stages by differential
            matchup_scores.sort(key = lambda x: -1 * math.inf if x[4] is None else x[4], reverse=True)

            context['matchupscores'] = matchup_scores

                


                

        return context