# game/forms.py
from django import forms
from .models import *

class CreateGameForm(forms.ModelForm):
    '''
    A from to create a new game.
    Users will choose the hider and seeker classes.
    Player will be set to the current user.
    Id will be auto generated.
    Current turn will be set to 0.
    ''' 
    class Meta:
        '''associate this form with Game model.'''
        model = Game
        fields = ['hider_class', 'seeker_class']

class CreateProfileForm(forms.ModelForm):
    '''
    A form to create a new profile.
    '''
    username = forms.CharField(max_length=120)
    email = forms.EmailField()
    class Meta:
        '''associate this form with Profile model.'''
        model = Profile
        fields = ['username', 'email']