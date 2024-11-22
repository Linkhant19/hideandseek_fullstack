# game/urls.py
# app specific URLs for the mini_fb app

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(r'', views.ShowAllCards.as_view(), name='show_all_cards'), # currently my main page
]