from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import pandas as pd

all_players = players.get_players()
# Define the player IDs
player_id1 = 203507  # Player 1 ID (e.g., Giannis Antetokounmpo)
player_id2 = 201935  # Player 2 ID (e.g., James Harden)

# Retrieve career statistics for Player 1
career_stats1 = playercareerstats.PlayerCareerStats(player_id=player_id1)
career_stats1 = career_stats1.get_data_frames()[0]  # Get the first data frame

# Retrieve career statistics for Player 2
career_stats2 = playercareerstats.PlayerCareerStats(player_id=player_id2)
career_stats2 = career_stats2.get_data_frames()[0]  # Get the first data frame

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Display the comparison
print("Career Statistics Comparison:")
print("-------------------------------------")
print(f"Player 1: {[x['full_name'] for x in all_players if x['id']==player_id1][0]}")
print(career_stats1[['PTS', 'REB', 'AST', 'STL', 'BLK']])
print("-------------------------------------")
print(f"Player 2: {[x['full_name'] for x in all_players if x['id']==player_id2][0]}")
print(career_stats2[['PTS', 'REB', 'AST', 'STL', 'BLK']])
