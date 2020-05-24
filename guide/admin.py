from django.contrib import admin

from .models import Character

# Register your models here.

class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'image')

admin.site.register(Character, CharacterAdmin)