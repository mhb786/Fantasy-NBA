from django.core.management.base import BaseCommand
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playerprofilev2
from nba_api.stats.endpoints import commonallplayers
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

            

            nba_player = NBAPlayer(first_name=first_name, last_name=last_name, team=team)
            
            nba_player.save()