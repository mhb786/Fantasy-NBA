from nba_api.stats.static import players
from nba_api.live.nba.endpoints

for x in players.get_players():
    print(x)