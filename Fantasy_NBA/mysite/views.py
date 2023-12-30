from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import NBAPlayer
import json
from django.core.serializers import serialize


# Create your views here.

@login_required
def home(response):
    return render(response, "mysite/home.html", {})

@login_required
def playercomparison(response, FN1, FN2):
    player1 = NBAPlayer.objects.get(first_name=FN1)
    player2 = NBAPlayer.objects.get(first_name=FN2)

    player1_stats = {
        'PPG': player1.PPG,
        'APG': player1.APG,
        'RPG': player1.RPG,
        'SPG': player1.SPG,
        'BPG': player1.BPG,
    }

    player2_stats = {
        'PPG': player2.PPG,
        'APG': player2.APG,
        'RPG': player2.RPG,
        'SPG': player2.SPG,
        'BPG': player2.BPG,
    }
    
    return render(response, 'mysite/playercomparison.html', {'player1_stats': player1_stats, 'player2_stats': player2_stats})
