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

import operator
import plotly
import plotly.graph_objects as go

# creating my views

class MainView(ListView):
    '''
    class-based view to show main page, inherited from ListView.
    '''
    model = Game
    template_name = 'game/main.html'
    context_object_name = 'games'

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
        '''
        override get method to add add_to_decks to context.
        '''
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

class CreateGameView(LoginRequiredMixin, CreateView):
    '''
    class-based view called CreateGameView to create a game, inherited from CreateView.
    Use the form from forms.py.
    '''
    form_class = CreateGameForm
    template_name = 'game/create_game.html'

    def get_login_url(self):
        '''return the URL to the login page'''
        return reverse('login')
    
    def get_success_url(self):
        '''return URL to redirect to the game page'''
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
        '''return URL to redirect to the show_profile page'''
        return reverse('game:show_profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # calculate games lost
        context['games_lost'] = self.object.games_played - self.object.games_won
        
        # Get the current profile player
        profile_player = self.object
        
        # Query the Game model to get the hider and seeker classes played by the profile player
        games = Game.objects.filter(player=profile_player)
        
        # Create lists to store the hider and seeker class names and counts
        hider_x = []
        hider_y = []
        seeker_x = []
        seeker_y = []
        
        # Loop through the games and count the occurrences of each hider and seeker class
        for game in games:
            hider_class = game.hider_class.class_name
            seeker_class = game.seeker_class.class_name
            
            if hider_class not in hider_x:
                hider_x.append(hider_class)
                hider_y.append(1)
            else:
                index = hider_x.index(hider_class)
                hider_y[index] += 1
            
            if seeker_class not in seeker_x:
                seeker_x.append(seeker_class)
                seeker_y.append(1)
            else:
                index = seeker_x.index(seeker_class)
                seeker_y[index] += 1

        print(hider_x, hider_y, seeker_x, seeker_y)
        
        # Create the pie charts
        fig_hider = fig_hider = fig_hider = go.Figure(go.Pie(labels=hider_x, values=hider_y, marker=dict(colors=['#FF69B4', '#33CC33', '#6666CC'])))
        fig_hider.update_layout(
            title="Hiders Played",
        )
        graph_pie_hider = plotly.offline.plot(fig_hider, auto_open=False, output_type='div')
        context['graph_pie_hider'] = graph_pie_hider
        
        fig_seeker = fig_seeker = fig_seeker = go.Figure(go.Pie(labels=seeker_x, values=seeker_y, marker=dict(colors=['#7a378b', '#741b47', '#f56fa1', '#fae7b5', '#caa8ea'])))
        fig_seeker.update_layout(
            title="Seekers Played",
        )
        graph_pie_seeker = plotly.offline.plot(fig_seeker, auto_open=False, output_type='div')
        context['graph_pie_seeker'] = graph_pie_seeker
        
        return context

    

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

class GameOverView(DetailView):
    '''
    class-based view called GameOverView to show a specific game, inherited from DetailView.
    '''
    model = Game
    template_name = 'game/game_over.html'
    context_object_name = 'game'

    def get(self, request, *args, **kwargs):
        '''
        override get to update the profile with the number of games played and games won.
        '''
        self.update_profile()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        '''
        override get_context_data and also allow result from game.html to be passed to game_over.html
        '''
        context = super().get_context_data(**kwargs)
        result = self.request.GET.get('result')
        if result == 'win':
            context['result'] = 'You won!'
        elif result == 'lose':
            context['result'] = 'You lost!'
        return context

    def update_profile(self):
        '''
        update the profile with the number of games played and games won.
        '''
        try:
            profile = self.request.user.profile

            # if result is win, update games won
            if self.request.GET.get('result') == 'win':
                profile.games_won += 1

            profile.games_played += 1
            profile.save()
        except Exception as e:
            print(f"Error updating profile: {e}")


    



    





    
