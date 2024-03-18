from django.contrib import admin
from .models import NBAPlayer, Team, Thread, Post, Profile, FantasyTeam

# Register your models here.

admin.site.register(NBAPlayer)
admin.site.register(Team)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(FantasyTeam)
