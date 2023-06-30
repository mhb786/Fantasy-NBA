from nba_api.stats.static import players

# Get all players
all_players = players.get_players()

# Extract player IDs
player_ids = [player for player in all_players]

# Print player IDs
for player_id in player_ids:
    print(player_id)
