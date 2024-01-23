from django.urls import path
from. import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
path("", login_required(views.home), name="home"),
path('playercomparison/', login_required(views.playercomparison), name="playercomparison"),
path('fixtures/', login_required(views.fixtures), name='fixtures'),
path('leagueleaders/', login_required(views.leagueleaders), name='leagueleaders')
]