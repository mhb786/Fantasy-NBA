from django.core.management.base import BaseCommand
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playerprofilev2
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.endpoints import playergamelog
from decimal import Decimal, InvalidOperation
from math import isnan
from mysite.models import NBAPlayer

class Command(BaseCommand):
    help = "import booms"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        nba_players = players.get_active_players()  

        for player in nba_players[400:]:
            stats = playergamelog.PlayerGameLog(player_id=player['id'], season='2022-23').get_data_frames()[0]
            player_profile = playerprofilev2.PlayerProfileV2(player_id=player['id']).get_data_frames()[0]

            first_name=player['first_name']
            last_name=player['last_name']
            try:
                team = teams.find_team_name_by_id(player_profile['TEAM_ID'].values[0])['full_name']
            except:
                team = 'Unknown'

            try:
                PPG = Decimal(round(stats['PTS'].mean(), 2))
                if isnan(PPG):
                    PPG = Decimal('0.0')
            except InvalidOperation:
                PPG = Decimal('0.0')

            try:
                APG = Decimal(round(stats['AST'].mean(), 2))
                if isnan(APG):
                    APG = Decimal('0.0')
            except InvalidOperation:
                APG = Decimal('0.0')

            try:
                RPG = Decimal(round(stats['REB'].mean(), 2))
                if isnan(RPG):
                    RPG = Decimal('0.0')
            except InvalidOperation:
                RPG = Decimal('0.0')

            try:
                SPG = Decimal(round(stats['STL'].mean(), 2))
                if isnan(SPG):
                    SPG = Decimal('0.0')
            except InvalidOperation:
                SPG = Decimal('0.0')

            try:
                BPG = Decimal(round(stats['BLK'].mean(), 2))
                if isnan(BPG):
                    BPG = Decimal('0.0')
            except InvalidOperation:
                BPG = Decimal('0.0')

            try:
                FG_PCT = Decimal(round(stats['FG_PCT'].mean(), 2))
                if isnan(FG_PCT):
                    FG_PCT = Decimal('0.0')
            except InvalidOperation:
                FG_PCT = Decimal('0.0')

            try:
                FG3_PCT = Decimal(round(stats['FG3_PCT'].mean(), 2))
                if isnan(FG3_PCT):
                    FG3_PCT = Decimal('0.0')
            except InvalidOperation:
                FG3_PCT = Decimal('0.0')

            try:
                FT_PCT = Decimal(round(stats['FT_PCT'].mean(), 2))
                if isnan(FT_PCT):
                    FT_PCT = Decimal('0.0')
            except InvalidOperation:
                FT_PCT = Decimal('0.0')

            try:
                MIN = Decimal(round(stats['MIN'].mean(), 2))
                if isnan(MIN):
                    MIN = Decimal('0.0')
            except InvalidOperation:
                MIN = Decimal('0.0')

            try:
                TOV = Decimal(round(stats['TOV'].mean(), 2))
                if isnan(TOV):
                    TOV = Decimal('0.0')
            except InvalidOperation:
                TOV = Decimal('0.0')

            nba_player = NBAPlayer(first_name=first_name, last_name=last_name, team=team, PPG=PPG, APG=APG, RPG=RPG,
            SPG=SPG, BPG=BPG, FG_PCT=FG_PCT, FG3_PCT=FG3_PCT, FT_PCT=FT_PCT, MIN=MIN, TOV=TOV)
            
            nba_player.save()