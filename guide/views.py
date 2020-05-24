from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from django.views import generic

from .models import Character

class HomepageView(generic.ListView):
    template_name = 'guide/homepage.html'
    context_object_name = 'character_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Character.objects.order_by('name')