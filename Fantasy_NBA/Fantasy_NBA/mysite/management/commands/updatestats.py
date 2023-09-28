from django.core.management.base import BaseCommand
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playerprofilev2
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.endpoints import playergamelog
from mysite.models import NBAPlayer

class Command(BaseCommand):
    help = "import booms"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        nba_players = players.get_active_players()  

        for player in nba_players:
            player_info = playercareerstats.PlayerCareerStats(player_id=player['id'])
            stats = player_info.get_data_frames()[0]
            player_profile = playerprofilev2.PlayerProfileV2(player_id=player['id']).get_data_frames()[0]

            first_name=player['first_name']
            last_name=player['last_name']
            try:
                team = teams.find_team_name_by_id(player_profile['TEAM_ID'].values[0])['full_name']
            except:
                team = 'Unknown'

            game_log_data = playergamelog.PlayerGameLog(player_id=player['id'], season='2022-23').get_data_frames()[0]
            PPG = round(game_log_data['PTS'].mean(), 2)
            APG = round(game_log_data['AST'].mean(), 2)
            RPG = round(game_log_data['REB'].mean(), 2)
            SPG = round(game_log_data['STL'].mean(), 2)
            BPG = round(game_log_data['BLK'].mean(), 2)
            FG_PCT = round(game_log_data['FG_PCT'].mean(), 2)
            FG3_PCT = round(game_log_data['FG3_PCT'].mean(), 2)
            FT_PCT = round(game_log_data['FT_PCT'].mean(), 2)
            MIN = round(game_log_data['MIN'].mean(), 2)
            TOV = round(game_log_data['TOV'].mean(), 2)

            nba_player = NBAPlayer(first_name=first_name, last_name=last_name, team=team, PPG=PPG, APG=APG, RPG=RPG,
            SPG=SPG, BPG=BPG, FG_PCT=FG_PCT, FG3_PCT=FG3_PCT, FT_PCT=FT_PCT, MIN=MIN, TOV=TOV)
            
            nba_player.save()