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
def home(request):
    if request.user.is_authenticated:
        url = "https://nba-latest-news.p.rapidapi.com/articles"
        try:
            favorite_team = request.user.profile.favorite_team.name.split()[-1]  # Extract last name
            querystring = {"team": favorite_team}

            headers = {
                "X-RapidAPI-Key": "1653a1f50amsha7a04d5574bda05p123149jsn718df4a7a999",
                "X-RapidAPI-Host": "nba-latest-news.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)
            if response.status_code == 200:
                news_data = response.json()
                nba_news = news_data[:5]
            else:
                nba_news = []
        
        except:
            favorite_team = ''
            nba_news = []

        return render(request, 'mysite/home.html', {'nba_news': nba_news, 'favorite_team': favorite_team})
    else:
        return render(request, 'mysite/home.html')


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

from nba_api.stats.static import players
from nba_api.stats.endpoints import PlayerFantasyProfileBarGraph

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

            player1_stats = prepare_player_stats(player1_stats, selected_stats)
            player2_stats = prepare_player_stats(player2_stats, selected_stats)

            player1_fantasystats, headers = get_fantasy_stats(player1_id)
            player2_fantasystats, headers = get_fantasy_stats(player2_id)
            print(player1_fantasystats, player2_fantasystats, headers)


            return render(request, 'mysite/playercomparison.html', {
                'form': form,
                'player1_name': player1_name,
                'player2_name': player2_name,
                'player1_stats': player1_stats,
                'player2_stats': player2_stats,
                'player1_fantasystats': player1_fantasystats,
                'player2_fantasystats': player2_fantasystats,
                'headers': headers,
                'selected_stats': selected_stats,
            })
        else:
            pass
    else:
        form = PlayerComparisonForm()

    return render(request, 'mysite/playercomparison_form.html', {'form': form})


def prepare_player_stats(stats_df, selected_stats):
    stats = []
    for stat in selected_stats:
        stats.append(stats_df[stat].values[0])
    return stats

def get_fantasy_stats(player_id):
    # Fetch fantasy stats for a player using PlayerFantasyProfileBarGraph endpoint
    # Implement this function to fetch fantasy stats for a given player ID
    # Example:
    fantasy_stats = PlayerFantasyProfileBarGraph(player_id).season_avg
    fantasy_stats_data = fantasy_stats.data
    headers = fantasy_stats.data['headers'][3:]
    
    # Extract relevant stats into an array
    player_fantasystats = [
        fantasy_stats_data['data'][0][3],
        fantasy_stats_data['data'][0][4],  # FAN_DUEL_PTS
        fantasy_stats_data['data'][0][5],  # NBA_FANTASY_PTS
        fantasy_stats_data['data'][0][6],  # PTS
        fantasy_stats_data['data'][0][7],  # REB
        fantasy_stats_data['data'][0][8],  # AST
        fantasy_stats_data['data'][0][9],  # FG3M
        fantasy_stats_data['data'][0][10], # FT_PCT
        fantasy_stats_data['data'][0][11], # STL
        fantasy_stats_data['data'][0][12], # BLK
        fantasy_stats_data['data'][0][13], # TOV
        fantasy_stats_data['data'][0][14], # FG_PCT
    ]

    return player_fantasystats, headers



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
    api_key = "1653a1f50amsha7a04d5574bda05p123149jsn718df4a7a999" 

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
from .forms import ThreadForm, PostForm
from django.db.models import Count

@login_required
def thread_list(request):
    query = request.GET.get('q')
    sort_option = request.GET.get('sort')

    threads = Thread.objects.all()
    threads = threads.order_by('-created_at')

    if query:
        threads = threads.filter(title__icontains=query)

    if sort_option == 'likes':
        threads = threads.annotate(num_upvotes=Count('upvotes')).order_by('-num_upvotes')
    if sort_option == 'recent':
        threads = threads.order_by('-created_at')


    return render(request, 'mysite/thread_list.html', {'threads': threads, 'sort_by': sort_option})



def upvote_thread(request, thread_id):
    thread = get_object_or_404(Thread, pk=thread_id)
    user = request.user
    
    if user in thread.upvotes.all():
        thread.upvotes.remove(user)  # Revoke upvote
    else:
        thread.upvotes.add(user)  # Upvote the thread
    
    return redirect('thread_list')

from .models import Thread
from .forms import ThreadForm

def edit_thread(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if request.method == 'POST':
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            form.save()
            return redirect('thread_detail', pk=pk)
    else:
        form = ThreadForm(instance=thread)
    return render(request, 'mysite/edit_thread.html', {'form': form, 'thread': thread})

def thread_detail(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    posts = thread.post_set.order_by('-created_at')
    return render(request, 'mysite/thread_detail.html', {'thread': thread, 'posts': posts})

@login_required
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            new_thread = form.save(commit=False)
            new_thread.creator = request.user  # Set the creator to the currently authenticated user
            new_thread.save()
            return redirect('thread_detail', pk=new_thread.pk)
    else:
        form = ThreadForm()
    return render(request, 'mysite/create_thread.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def create_post(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.thread = thread
            new_post.author = request.user
            new_post.save()
            return redirect('thread_detail', pk=thread.pk)
    else:
        form = PostForm()
    return render(request, 'mysite/create_post.html', {'form': form, 'thread': thread})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user == post.author:
        thread = post.thread
        post.delete()
        return redirect('thread_detail', pk=thread.pk)


from .forms import PostForm

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('thread_detail', pk=post.thread.pk)  # Redirect to thread detail
    else:
        form = PostForm(instance=post)
    return render(request, 'mysite/edit_post.html', {'form': form})


def news(request):
    player_name = request.GET.get('q', '')
    url = "https://nba-latest-news.p.rapidapi.com/articles"

    headers = {
        "X-RapidAPI-Key": "1653a1f50amsha7a04d5574bda05p123149jsn718df4a7a999",
        "X-RapidAPI-Host": "nba-latest-news.p.rapidapi.com"
    }

    querystring = {"player": player_name} 

    response = requests.get(url, headers=headers, params=querystring)
    news_data = response.json()

    return render(request, 'mysite/news.html', {'news_data': news_data})


from .models import Profile, Team
from django.contrib import messages
from .forms import ProfileUpdateForm, UserUpdateForm

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            profile = p_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    teams = Team.objects.all()  # Assuming you have a Team model
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'teams': teams
    }
    return render(request, 'mysite/profile.html', context)

from .models import FantasyTeam

@login_required
def teambuilder(request):
    fantasy_team = FantasyTeam.objects.get(user=request.user)
    starters = [fantasy_team.player1, fantasy_team.player2, fantasy_team.player3, fantasy_team.player4, fantasy_team.player5]
    bench_players = [fantasy_team.player6, fantasy_team.player7, fantasy_team.player8, fantasy_team.player9, fantasy_team.player10]

    for player in starters + bench_players:
        player.team_info = Team.objects.filter(name=player.team).first()

    return render(request, 'mysite/teambuilder.html', {'starters': starters, 'bench_players': bench_players})

from .forms import UpdateTeamForm

@login_required
def teambuilder_update(request):
    user = request.user
    fantasy_team = FantasyTeam.objects.get(user=user)

    if request.method == 'POST':
        form = UpdateTeamForm(request.POST, instance=fantasy_team)
        if form.is_valid():
            form.save()
            return redirect('teambuilder')  # Redirect the user to the team builder page
    else:
        form = UpdateTeamForm(instance=fantasy_team)

    return render(request, 'mysite/teambuilder_update.html', {'form': form})

@login_required
def delete_thread(request, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if thread.creator == request.user:
        thread.delete()
    return redirect('forum')

@login_required
def team_list(request):
    teams = Team.objects.all()
    return render(request, 'mysite/team_list.html', {'teams': teams})


def get_stats(player_id):
    try:
        fantasy_stats = PlayerFantasyProfileBarGraph(player_id).season_avg
        fantasy_stats_data = fantasy_stats.data
        
        # Extract relevant stats into an array
        player_fantasystats = [
            fantasy_stats_data['data'][0][4],  # FAN_DUEL_PTS
            fantasy_stats_data['data'][0][5],  # NBA_FANTASY_PTS
            fantasy_stats_data['data'][0][6],  # PTS
            fantasy_stats_data['data'][0][7],  # REB
            fantasy_stats_data['data'][0][8],  # AST
            fantasy_stats_data['data'][0][9],  # FG3M
            fantasy_stats_data['data'][0][10], # FT_PCT
            fantasy_stats_data['data'][0][11], # STL
            fantasy_stats_data['data'][0][12], # BLK
            fantasy_stats_data['data'][0][13], # TOV
            fantasy_stats_data['data'][0][14], # FG_PCT
        ]

        return player_fantasystats
    except:
        return []

def team_profile(request, team_id):
    team = Team.objects.get(team_id=team_id)
    players = NBAPlayer.objects.filter(team=team.name)

    players_with_stats = []
    for player in players:
        player_name = player.first_name + " " + player.last_name
        player_id = get_player_id_by_full_name(player_name)
        stats = get_stats(player_id)
        if fantasy_stats != []:
            player_stats = {
                'first_name': player.first_name,
                'last_name': player.last_name,
                'stats': stats
            }
            players_with_stats.append(player_stats)

    return render(request, 'mysite/team_profile.html', {'team': team, 'players_with_stats': players_with_stats})

