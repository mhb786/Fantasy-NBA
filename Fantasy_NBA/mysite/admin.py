from django.contrib import admin
from .models import NBAPlayer, Fixture

# Register your models here.

admin.site.register(NBAPlayer)
admin.site.register(Fixture)

