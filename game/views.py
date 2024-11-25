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
