# game/views.py

from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse

from . models import *

from . forms import *

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse
import random

# creating my views

class ShowAllCards(ListView):
    '''
    class-based view to show all cards, inherited from ListView.
    '''
    model = Card
    template_name = 'game/show_all_cards.html'
    context_object_name = 'cards'

    def get_queryset(self):
        '''
        override get_queryset to order cards by card_type in get form
        '''
        qs = super().get_queryset()

        # check if card_type is in request.GET --> returns cards of that type
        if 'card_type' in self.request.GET:
            card_type = self.request.GET['card_type']
            qs = qs.filter(card_type__icontains=card_type)

        # check if the card_name from request.GET matches first letters of card_name
        if 'card_name' in self.request.GET:
            card_name = self.request.GET['card_name']
            qs = qs.filter(card_name__startswith=card_name)

        return qs

class ShowAllHiders(ListView):
    '''
    class-based view to show all heroes, inherited from ListView.
    '''
    model = Hider
    template_name = 'game/show_all_hiders.html'
    context_object_name = 'hiders'

class ShowAllSeekers(ListView):
    '''
    class-based view to show all heroes, inherited from ListView.
    '''
    model = Seeker
    template_name = 'game/show_all_seekers.html'
    context_object_name = 'seekers'

class ShowHiderView(DetailView):
    '''
    class-based view called ShowHiderView to show a specific hider, inherited from DetailView.
    '''
    model = Hider
    template_name = 'game/show_hider.html'
    context_object_name = 'hider'

    # I want to use AddToDeck model to show cards that are added to this Hider's deck
    def get_context_data(self, **kwargs):
        '''
        override get_context_data to add add_to_decks to context
        '''
        context = super().get_context_data(**kwargs)
        context['add_to_decks'] = AddToDeck.objects.filter(hider_class=self.object)
        return context

class ShowSeekerView(DetailView):
    '''
    class-based view called ShowSeekerView to show a specific seeker, inherited from DetailView.
    '''
    model = Seeker
    template_name = 'game/show_seeker.html'
    context_object_name = 'seeker'

    # I want to use AddToDeck model to show cards that are added to this Seeker's deck
    def get_context_data(self, **kwargs):
        '''
        override get_context_data to add add_to_decks to context
        '''
        context = super().get_context_data(**kwargs)
        context['add_to_decks'] = AddToDeck.objects.filter(seeker_class=self.object)
        return context


class GameView(View):
    '''
    class-based view called GameView to show a specific game, inherited from View.
    '''
    model = Game
    template_name = 'game/game.html'
    context_object_name = 'game'

    def get(self, request, pk, *args, **kwargs):
        context = self.get_context_data(pk)
        return render(request, self.template_name, context)

    def get_context_data(self, pk):
        '''
        override get_context_data to add add_to_decks to context.
        make a list of all cards of this game's hider.
        make a list of all cards of this game's seeker.
        '''
        context = {}
        context['game'] = Game.objects.get(pk=pk)
        context['add_to_decks'] = AddToDeck.objects.all()
        context['hider_cards'] = Card.objects.filter(addtodeck__hider_class=context['game'].hider_class)
        context['seeker_cards'] = Card.objects.filter(addtodeck__seeker_class=context['game'].seeker_class)
        return context

class CreateGameView(CreateView):
    '''
    class-based view called CreateGameView to create a game, inherited from CreateView.
    Use the form from forms.py.
    '''
    form_class = CreateGameForm
    template_name = 'game/create_game.html'
    
    def get_success_url(self):
        return reverse('game:game', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        ''' this method exectues after form submission.'''
        game = form.save(commit=False)
        game.player = self.request.user.profile
        game.save()
        return redirect('game', pk=game.pk)


class ShowProfileView(DetailView):
    '''
    class-based view called ShowProfileView to show a specific profile, inherited from DetailView.
    '''
    model = Profile
    template_name = 'game/show_profile.html'
    context_object_name = 'profile'

    def get_success_url(self):
        return reverse('game:show_profile', kwargs={'pk': self.object.pk})

class CreateProfileView(CreateView):
    '''
    class-based view called CreateProfileView to create a profile, inherited from CreateView.
    Use the form from forms.py.
    '''
    form_class = CreateProfileForm
    template_name = 'game/create_profile.html'

    def get_login_url(self):
        '''return the URL to the login page'''
        return reverse('login')

    def get_success_url(self):
        '''return URL to redirect to the show_profile page'''
        return reverse('game:show_profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        '''
        provides context for the template
        '''
        context = super().get_context_data(**kwargs)
        context['form2'] = UserCreationForm(self.request.POST)
        return context

    def form_valid(self, form):
        ''' this method exectues after form submission.'''

        form2 = UserCreationForm(self.request.POST)

        if not form2.is_valid():
            return super().form_invalid(form2)

        # attach the user to the profile creation form
        user = form2.save()
        profile = form.instance
        profile.user = user
        profile.save()
        login(self.request, user)
        return redirect('show_profile', pk=profile.pk)

    





    
