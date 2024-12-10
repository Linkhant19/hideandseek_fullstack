# game/admin.py

from django.contrib import admin

# Register your models here.
from game.models import *

# I want to access these models from the admin interface
admin.site.register(Profile)
admin.site.register(Card)
admin.site.register(Hider)
admin.site.register(Seeker)
admin.site.register(AddToDeck)
admin.site.register(Game)
admin.site.register(UploadCard)
