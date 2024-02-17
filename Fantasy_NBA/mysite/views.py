from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import NBAPlayer
from django.core.serializers import serialize
from .forms import PlayerComparisonForm, NBAStatsForm
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import pandas as pd
from nba_api.stats.endpoints.leagueleaders import LeagueLeaders
import requests


@login_required
def home(response):
    return render(response, "mysite/home.html", {})

def get_player_id_by_full_name(full_name):
    player_list = players.get_players()

    matching_players = players.find_players_by_full_name(full_name)

    if matching_players:
        player = matching_players[0]
        return player['id']
    else:
        print(f"No player found with the full name: {full_name}")
        return None


def get_player_stats(player_id, per_mode='PerGame', league_id='', season='2023'):
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id, per_mode36=per_mode, league_id_nullable=league_id)
    player_stats = career_stats.get_data_frames()[0]
    season_stats = player_stats[player_stats['SEASON_ID'] == f"{season}-{int(season[-2:]) + 1}"]
    return season_stats


@login_required
def playercomparison(request):
    if request.method == 'POST':
        form = PlayerComparisonForm(request.POST)

        if form.is_valid():
            player1 = form.cleaned_data['player1']
            player2 = form.cleaned_data['player2']
            selected_stats = form.cleaned_data['selected_stats']

            player1_name = player1.first_name + " " + player1.last_name
            player2_name = player2.first_name + " " + player2.last_name

            player1_id = get_player_id_by_full_name(player1_name)
            player2_id = get_player_id_by_full_name(player2_name)

            player1_stats = get_player_stats(player1_id)
            player2_stats = get_player_stats(player2_id)

            player1_stats_dict = prepare_player_stats(player1_stats, selected_stats, player1_name)
            player2_stats_dict = prepare_player_stats(player2_stats, selected_stats, player2_name)

            return render(request, 'mysite/playercomparison.html', {
                'form': form,
                'player1_stats': player1_stats_dict,
                'player2_stats': player2_stats_dict,
                'selected_stats': selected_stats,
            })
        else:
            pass
    else:
        form = PlayerComparisonForm()

    return render(request, 'mysite/playercomparison_form.html', {'form': form})


def prepare_player_stats(stats_df, selected_stats, player_name):
    stats_dict = {'player_name': player_name}
    for stat in selected_stats:
        stats_dict[stat] = stats_df[stat].values[0]
    return stats_dict


def get_fixtures_for_date(api_key, date):
    url = "https://api-nba-v1.p.rapidapi.com/games"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }
    query_params = {"date": date}

    response = requests.get(url, headers=headers, params=query_params)

    if response.status_code == 200:
        fixtures_data = response.json()
        return fixtures_data.get('response', [])
    else:
        print(f"Error: {response.status_code}")
        return []


@login_required
def fixtures(request):
    api_key = "1653a1f50amsha7a04d5574bda05p123149jsn718df4a7a999"  # Replace with your actual RapidAPI key

    if request.method == 'POST':
        specific_date = request.POST.get('date')
        fixtures = get_fixtures_for_date(api_key, specific_date)
        return render(request, 'mysite/fixtures.html', {'fixtures': fixtures, 'specific_date': specific_date})
    else:
        return render(request, 'mysite/fixtures.html')


from nba_api.stats.endpoints import LeagueLeaders

@login_required
def leagueleaders(request):
    if request.method == 'POST':
        form = NBAStatsForm(request.POST)
        if form.is_valid():
            season = form.cleaned_data['season']
            stat_category = form.cleaned_data['stat_category']

            league_leaders = LeagueLeaders(season=season, stat_category_abbreviation=stat_category)
            data = league_leaders.league_leaders.get_dict()
            players_data = data["data"][:20]

            context = {
                'form': form,
                'players_data': players_data,
                'stat_category': stat_category,
                'season': season,
            }
            return render(request, 'mysite/leagueleaders.html', context)
    else:
        form = NBAStatsForm()

    context = {'form': form}
    return render(request, 'mysite/leagueleaders.html', context)

@login_required
def games(request):
    return render(request, 'mysite/games.html')

@login_required
def standings(request):
    url = "https://api-nba-v1.p.rapidapi.com/standings"
    querystring = {"league": "standard", "season": "2023"}
    headers = {
        "X-RapidAPI-Key": "1653a1f50amsha7a04d5574bda05p123149jsn718df4a7a999",
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()

        standings_data = response.json()

        if "response" in standings_data:
            standings = standings_data["response"]
            rank_list = [rank for rank in range(1, 16)]
            context = {"standings": standings, "rank_list": rank_list}
            return render(request, 'mysite/standings.html', context)

        else:
            error_message = "No standings data available."

    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching standings: {e}"

    context = {"error_message": error_message}
    return render(request, 'mysite/standings.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Thread, Post
from .forms import ThreadForm, PostForm  # Assuming you have these forms.

def thread_list(request):
    threads = Thread.objects.all()
    return render(request, 'mysite/thread_list.html', {'threads': threads})

def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = thread.post_set.all()
    return render(request, 'mysite/thread_detail.html', {'thread': thread, 'posts': posts})

def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            new_thread = form.save()
            return redirect('thread_detail', pk=new_thread.pk)  # Redirect to the newly created thread's detail view
    else:
        form = ThreadForm()
    return render(request, 'mysite/create_thread.html', {'form': form})

def create_post(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.thread = thread
            new_post.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = PostForm()
    return render(request, 'mysite/create_post.html', {'form': form, 'thread': thread})
