from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import NBAPlayer
from django.core.serializers import serialize
from .forms import PlayerComparisonForm, SeasonForm
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


def get_player_stats(player_id, per_mode='Totals', league_id='', season='2023'):
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id, per_mode36=per_mode, league_id_nullable=league_id)
    player_stats = career_stats.get_data_frames()[0]
    season_stats = player_stats[player_stats['SEASON_ID'] == f"{season}-{int(season[-2:]) + 1}"]
    return season_stats

from nba_api.stats.library.parameters import (
    LeagueID,
    PerMode48,
    Scope,
    Season,
    SeasonTypeAllStar,
    StatCategoryAbbreviation,
)

@login_required
def playercomparison(request):
    if request.method == 'POST':
        form = PlayerComparisonForm(request.POST)

        if form.is_valid():
            player1 = form.cleaned_data['player1']
            player2 = form.cleaned_data['player2']

            player1_name = player1.first_name + " " + player1.last_name
            player2_name = player2.first_name + " " + player2 .last_name

            player1_id = get_player_id_by_full_name(player1_name)
            player2_id = get_player_id_by_full_name(player2_name)

            if player1_id is not None and player2_id is not None:
                player1_stats = get_player_stats(player1_id)
                player2_stats = get_player_stats(player2_id)

                if not player1_stats.empty and not player2_stats.empty:
                    player1_stats_dict = {
                        'PPG': player1_stats['PTS'].values[0] / player1_stats['GP'].values[0],
                        'APG': player1_stats['AST'].values[0] / player1_stats['GP'].values[0],
                        'RPG': player1_stats['REB'].values[0] / player1_stats['GP'].values[0],
                        'SPG': player1_stats['STL'].values[0] / player1_stats['GP'].values[0],
                        'BPG': player1_stats['BLK'].values[0] / player1_stats['GP'].values[0],
                        'player_name': player1_name,
                    }

                    player2_stats_dict = {
                        'PPG': player2_stats['PTS'].values[0] / player2_stats['GP'].values[0],
                        'APG': player2_stats['AST'].values[0] / player2_stats['GP'].values[0],
                        'RPG': player2_stats['REB'].values[0] / player2_stats['GP'].values[0],
                        'SPG': player2_stats['STL'].values[0] / player2_stats['GP'].values[0],
                        'BPG': player2_stats['BLK'].values[0] / player2_stats['GP'].values[0],
                        'player_name': player2_name,
                    }

                    return render(request, 'mysite/playercomparison.html', {
                        'form': form,
                        'player1_stats': player1_stats_dict,
                        'player2_stats': player2_stats_dict,
                    })
                else:
                    error_message = "Error: Unable to retrieve statistics for one or both players."
            else:
                error_message = "Error: One or both players not found."
            
            return render(request, 'mysite/playercomparison_form.html', {
                'form': form,
                'error_message': error_message,
            })

    else:
        form = PlayerComparisonForm()

    return render(request, 'mysite/playercomparison_form.html', {'form': form})


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

def get_top_players(season, stat):
    league_leaders = LeagueLeaders(
        league_id=LeagueID.default,
        per_mode48=PerMode48.default,
        scope=Scope.default,
        season=season,
        season_type_all_star=SeasonTypeAllStar.default,
        stat_category_abbreviation=stat,
    )

    response = league_leaders.get_data_frames()
    top5 = response[0][["PLAYER", stat]][:5]
    return top5.itertuples(index=False, name=None)



@login_required
def leagueleaders(request):
    if request.method == 'POST':
        form = SeasonForm(request.POST)

        if form.is_valid():
            selected_season = form.cleaned_data['selected_season']

            # Get top players for the selected season
            top_scorers = get_top_players(selected_season, 'PTS')
            top_assist_makers = get_top_players(selected_season, 'AST')
            top_rebounders = get_top_players(selected_season, 'REB')

            context = {
                'selected_season': selected_season,
                'top_scorers': top_scorers,
                'top_assist_makers': top_assist_makers,
                'top_rebounders': top_rebounders,
            }

            return render(request, 'mysite/leagueleaders.html', context)
    else:
        form = SeasonForm()

    return render(request, 'mysite/leagueleaders.html', {'form': form})