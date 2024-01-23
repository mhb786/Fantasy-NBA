from django.contrib import admin
from .models import NBAPlayer, Fixture, Team

# Register your models here.

admin.site.register(NBAPlayer)
admin.site.register(Fixture)
admin.site.register(Team)

