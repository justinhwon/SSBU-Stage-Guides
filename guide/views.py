from django.shortcuts import get_object_or_404, render
import uuid

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
        #Return all characters ordered alphabetically.
        return Character.objects.order_by('name')



class HomepageView(generic.TemplateView):
    template_name = 'guide/homepagetemplate.html'

class PrivacyView(generic.TemplateView):
    template_name = 'guide/privacypolicy.html'

class CookieView(generic.TemplateView):
    template_name = 'guide/cookiepolicy.html'

class TermsView(generic.TemplateView):
    template_name = 'guide/termsconditions.html'


# helper function for CharacterView to map variable names to readable names
def varToName(d, votes):
    mappedDict = []
    for key, value in d.items():
        img = ''
        # map to readable names
        if key == 'battlefield__avg':
            key = 'Battlefield'
            img = 'guide/stage_images/' + 'battlefield.png'
            #img = "https://www.ssbwiki.com/images/thumb/8/86/SSBU-Battlefield.png/300px-SSBU-Battlefield.png"
            numVotes = votes.filter(battlefield__isnull=False).count()
        elif key == 'final_destination__avg':
            key = 'Final Destination'
            img = 'guide/stage_images/' + 'final_destination.jpg'
            #img = "https://www.ssbwiki.com/images/thumb/9/91/SSBU-Final_Destination.jpg/300px-SSBU-Final_Destination.jpg"
            numVotes = votes.filter(final_destination__isnull=False).count()
        elif key == 'pokemon_stadium__avg':
            key = 'Pokémon Stadium 2'
            img = 'guide/stage_images/' + 'pokemon_stadium.png'
            #img = "https://www.ssbwiki.com/images/thumb/7/73/SSBU-Pok%C3%A9mon_Stadium_2.png/300px-SSBU-Pok%C3%A9mon_Stadium_2.png"
            numVotes = votes.filter(pokemon_stadium__isnull=False).count()
        elif key == 'small_battlefield__avg':
            key = 'Small Battlefield'
            img = 'guide/stage_images/' + 'small_battlefield.jpg'
            #img = "https://www.ssbwiki.com/images/thumb/7/7e/SSBU-Small-Battlefield.jpg/300px-SSBU-Small-Battlefield.jpg"
            numVotes = votes.filter(small_battlefield__isnull=False).count()
        elif key == 'smashville__avg':
            key = 'Smashville'
            img = 'guide/stage_images/' + 'smashville.png'
            #img = "https://www.ssbwiki.com/images/thumb/0/02/SSBU-Smashville.png/300px-SSBU-Smashville.png"
            numVotes = votes.filter(smashville__isnull=False).count()
        elif key == 'lylat__avg':
            key = 'Lylat Cruise'
            img = 'guide/stage_images/' + 'lylat.jpg'
            #img = "https://www.ssbwiki.com/images/thumb/5/5f/SSBU-Lylat_Cruise.jpg/300px-SSBU-Lylat_Cruise.jpg"
            numVotes = votes.filter(lylat__isnull=False).count()
        elif key == 'town__avg':
            key = 'Town and City'
            img = 'guide/stage_images/' + 'town.png'
            #img = "https://www.ssbwiki.com/images/thumb/2/26/SSBU-Town_and_City.png/300px-SSBU-Town_and_City.png"
            numVotes = votes.filter(town__isnull=False).count()
        elif key == 'kalos__avg':
            key = 'Kalos'
            img = 'guide/stage_images/' + 'kalos.png'
            #img = "https://www.ssbwiki.com/images/thumb/b/bf/SSBU-Kalos_Pok%C3%A9mon_League.png/300px-SSBU-Kalos_Pok%C3%A9mon_League.png"
            numVotes = votes.filter(kalos__isnull=False).count()
        elif key == 'yoshi_story__avg':
            key = "Yoshi's Story"
            img = 'guide/stage_images/' + 'yoshi_story.png'
            #img = "https://www.ssbwiki.com/images/thumb/0/0c/SSBU-Yoshi%27s_Story.png/300px-SSBU-Yoshi%27s_Story.png"
            numVotes = votes.filter(yoshi_story__isnull=False).count()
        elif key == 'yoshi_island__avg':
            key = "Yoshi's Island"
            img = 'guide/stage_images/' + 'yoshi_island.png'
            #img = "https://www.ssbwiki.com/images/thumb/7/7b/SSBU-Yoshi%27s_Island_%28SSBB%29.png/300px-SSBU-Yoshi%27s_Island_%28SSBB%29.png"
            numVotes = votes.filter(yoshi_island__isnull=False).count()
        elif key == 'unova__avg':
            key = "Unova"
            img = 'guide/stage_images/' + 'unova.png'
            #img = "https://www.ssbwiki.com/images/thumb/b/b2/SSBU-Unova_Pok%C3%A9mon_League.png/300px-SSBU-Unova_Pok%C3%A9mon_League.png"
            numVotes = votes.filter(unova__isnull=False).count()
        temp = [key, value, img, numVotes]
        mappedDict.append(temp)
    return mappedDict

# displays stage rankings for a character
class CharacterView(generic.DetailView):
    model = Character
    template_name = 'guide/character.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Check cookies to see whether user voted on character or not
        if str(context['character']) in self.request.session and self.request.session[str(context['character'])] == True:
            context['voted_already'] = True
        else:
            context['voted_already'] = False
        #for key, value in self.request.session.items():
        #    print('{} => {}'.format(key, value))
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
            vote_avgs_dict = votes.aggregate(Avg('battlefield'), Avg('final_destination'), Avg('pokemon_stadium'), Avg('small_battlefield'),
                Avg('smashville'), Avg('town'), Avg('lylat'), Avg('kalos'), Avg('yoshi_story'), 
                Avg('yoshi_island'), Avg('unova'))

            # convert to list of form (stage_name, score)
            vote_avgs = varToName(vote_avgs_dict, votes)

            

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
    
    battlefield = forms.ChoiceField(label='Battlefield', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    final_destination = forms.ChoiceField(label='Final Destination', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    pokemon_stadium = forms.ChoiceField(label='Pokémon Stadium 2', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    small_battlefield = forms.ChoiceField(label='Small Battlefield', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    smashville = forms.ChoiceField(label='Smashville', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    town = forms.ChoiceField(label='Town and City', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    lylat = forms.ChoiceField(label='Lylat Cruise', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    kalos = forms.ChoiceField(label='Kalos', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    yoshi_story = forms.ChoiceField(label="Yoshi's Story", choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    yoshi_island = forms.ChoiceField(label="Yoshi's Island", choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    unova = forms.ChoiceField(label='Unova', choices=VOTEVALUES, widget=forms.RadioSelect, required=False)
    sessionid = forms.CharField(label='sessionid', widget=forms.HiddenInput)
    

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

    def clean_small_battlefield(self):
        small_battlefield = self.cleaned_data['small_battlefield']
        if not small_battlefield:
            small_battlefield = None
        elif int(small_battlefield) > 3 or int(small_battlefield) < -3:
            raise forms.ValidationError("Only scores between -3 and 3 allowed.")
        return small_battlefield

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
        fields = ['character', 'sessionid', 'battlefield', 'final_destination', 'pokemon_stadium', 'small_battlefield', 'smashville',
        'town', 'lylat', 'kalos', 'yoshi_story', 'yoshi_island', 'unova']
        widgets = {'character': forms.HiddenInput(), 'sessionid': forms.HiddenInput()}


# creates a new vote for the user
class VoteView(generic.CreateView):
    template_name = 'guide/vote.html'
    form_class = VoteModelForm
    #success_url = reverse('guide:character')

    def get_success_url(self, **kwargs):
        self.request.session[self.kwargs['charactername']] = True
        return reverse('guide:character', args=[self.kwargs['charactername']])

    def get_initial(self, *args, **kwargs):
        initial = super(VoteView, self).get_initial(**kwargs)
        initial['character'] = self.kwargs['charactername']

        # if no session then create it
        if not self.request.session.session_key:
            self.request.session.create()
            # set a uuid instead of session id (since Firefox doesn't seem to accept empty cookies)
            self.request.session['uuid'] = str(uuid.uuid4().hex)
        #initial['sessionid'] = str(self.request.session.session_key)[0:32]
        
        # if there's no uuid set it
        if 'uuid' not in self.request.session:
            self.request.session['uuid'] = str(uuid.uuid4().hex)

        initial['sessionid'] = self.request.session['uuid']
        #print('session id: ', initial['sessionid'])
        #print(initial)

        return initial

    def get_context_data(self, **kwargs):
        context = super(VoteView, self).get_context_data(**kwargs)
        context['character'] = get_object_or_404(Character, pk=self.kwargs['charactername'])
        return context

# updates a vote user already made
class RevoteView(generic.UpdateView):
    template_name = 'guide/revote.html'
    form_class = VoteModelForm
    context_object_name = 'prevVote'

    def get_context_data(self, **kwargs):
        context = super(RevoteView, self).get_context_data(**kwargs)
        context['character'] = get_object_or_404(Character, pk=self.kwargs['charactername'])
        return context
    
    def get_success_url(self, **kwargs):
        return reverse('guide:character', args=[self.kwargs['charactername']])

    #get object
    def get_object(self, queryset=None, **kwargs): 
        return Vote.objects.filter(sessionid=self.request.session['uuid']).filter(character=self.kwargs['charactername']).first()

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
            vote_avgs_dict = votes.aggregate(Avg('battlefield'), Avg('final_destination'), Avg('pokemon_stadium'), Avg('small_battlefield'),
                Avg('smashville'), Avg('town'), Avg('lylat'), Avg('kalos'), Avg('yoshi_story'), 
                Avg('yoshi_island'), Avg('unova'))

            # convert to list of form (stage_name, score)
            vote_avgs = varToName(vote_avgs_dict, votes)

            

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
            opp_vote_avgs_dict = opp_votes.aggregate(Avg('battlefield'), Avg('final_destination'), Avg('pokemon_stadium'), Avg('small_battlefield'),
                Avg('smashville'), Avg('town'), Avg('lylat'), Avg('kalos'), Avg('yoshi_story'), 
                Avg('yoshi_island'), Avg('unova'))

            # convert to list of form (stage_name, score)
            opp_vote_avgs = varToName(opp_vote_avgs_dict, opp_votes)

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
                if score is not None and opp_score is not None:
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