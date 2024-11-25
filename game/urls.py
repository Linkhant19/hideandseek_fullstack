# game/urls.py
# app specific URLs for the mini_fb app

from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(r'', views.ShowAllCards.as_view(), name='show_all_cards'), # currently my main page
    path(r'hiders/', views.ShowAllHiders.as_view(), name='show_all_hiders'), # page for showing all hiders
    path(r'seekers/', views.ShowAllSeekers.as_view(), name='show_all_seekers'), # page for showing all seekers
]