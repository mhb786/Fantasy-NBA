from django.urls import path
from. import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
path("", login_required(views.home), name="home"),
path('playercomparison/', login_required(views.playercomparison), name="playercomparison"),
path('fixtures/', login_required(views.fixtures), name='fixtures'),
path('leagueleaders/', login_required(views.leagueleaders), name='leagueleaders'),
path('standings/', login_required(views.standings), name='standings'),
path('games/', login_required(views.games), name='games'),
path('forum', views.thread_list, name='thread_list'),
path('thread/<int:pk>/', views.thread_detail, name='thread_detail'),
path('new_thread/', views.create_thread, name='create_thread'),
path('thread/<int:pk>/new_post/', views.create_post, name='create_post'),
]