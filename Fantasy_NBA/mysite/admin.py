from django.contrib import admin
from .models import NBAPlayer, Team, Thread, Post

# Register your models here.

admin.site.register(NBAPlayer)
admin.site.register(Team)
admin.site.register(Thread)
admin.site.register(Post)

