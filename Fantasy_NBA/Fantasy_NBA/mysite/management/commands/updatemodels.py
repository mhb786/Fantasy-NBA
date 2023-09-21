from django.core.management.base import BaseCommand
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats
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
            player_profile = playerprofilev2.PlayerProfileV2(player_id=player['id'])
            player_profile_info = player_profile.get_data_frames()[0]
        
            # Create or update the player in the database
            nba_player, created = NBAPlayer.objects.get_or_create(
                first_name=player['first_name'],
                last_name=player['last_name'],
                team=teams.find_team_name_by_id(player_profile_info['TEAM_ID'].values[0]),
            )
            
            # Update statistics fields
            if not created:
                nba_player.points_per_game = stats['PTS'].mean() if 'PTS' in stats else None
                nba_player.assists_per_game = stats['AST'].mean() if 'AST' in stats else None
                nba_player.rebounds_per_game = stats['REB'].mean() if 'REB' in stats else None
            
            nba_player.save()