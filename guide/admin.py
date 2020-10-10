from django.contrib import admin

from .models import Character, Vote

# Register your models here.

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'image')
    #list_editable = ( 'number', 'image')

class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'sessionid', 'timestampUpdated', 'timestampCreated', 'character', 'battlefield','small_battlefield','final_destination','pokemon_stadium','smashville','town','lylat','kalos','yoshi_story','yoshi_island','unova')
    search_fields = ['character__name']

admin.site.register(Character, CharacterAdmin)
admin.site.register(Vote, VoteAdmin)