# game/views.py

from typing import Any
from django.shortcuts import render, redirect
from django.urls import reverse

from . models import *

# i dont have forms yet
# from . forms import *

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
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
        context = super().get_context_data(**kwargs)
        context['add_to_decks'] = AddToDeck.objects.filter(seeker_class=self.object)
        return context

    
