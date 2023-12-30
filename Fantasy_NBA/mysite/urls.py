from django.urls import path
from. import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
path("", login_required(views.home), name="home"),
path('compare/<str:FN1>/<str:FN2>/', login_required(views.playercomparison), name="playercomparison")
]