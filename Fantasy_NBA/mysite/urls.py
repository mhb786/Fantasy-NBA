from django.urls import path
from. import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path("", login_required(views.home), name="home"),
path('playercomparison/', login_required(views.playercomparison), name="playercomparison"),
path('fixtures/', login_required(views.fixtures), name='fixtures'),
path('leagueleaders/', login_required(views.leagueleaders), name='leagueleaders'),
path('standings/', login_required(views.standings), name='standings'),
path('games/', login_required(views.games), name='games'),
path('news/', login_required(views.news), name='news'),
path('forum', login_required(views.thread_list), name='thread_list'),
path('thread/<int:pk>/', login_required(views.thread_detail), name='thread_detail'),
path('new_thread/', login_required(views.create_thread), name='create_thread'),
path('thread/<int:pk>/new_post/', login_required(views.create_post), name='create_post'),
path('threads/<int:pk>/delete/', login_required(views.delete_thread), name='delete_thread'),
path('profile/', login_required(views.profile), name='profile'),
path('teambuilder/', login_required(views.teambuilder), name='teambuilder'),
path('teambuilder_update/', login_required(views.teambuilder_update), name='teambuilder_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)