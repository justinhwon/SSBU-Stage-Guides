from django.contrib import admin

from .models import Character, Vote

# Register your models here.

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'image')
    #list_editable = ( 'number', 'image')

admin.site.register(Character, CharacterAdmin)
admin.site.register(Vote)