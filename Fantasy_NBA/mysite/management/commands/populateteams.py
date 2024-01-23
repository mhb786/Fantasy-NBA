# yourapp/management/commands/fetch_nba_teams.py

import requests
from django.core.management.base import BaseCommand
from mysite.models import Team

class Command(BaseCommand):
    help = 'Fetch and save NBA teams from API'

    def handle(self, *args, **options):
        api_url = "https://api-nba-v1.p.rapidapi.com/teams/"
        headers = {
            "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com",
            "X-RapidAPI-Key": "1653a1f50amsha7a04d5574bda05p123149jsn718df4a7a999",
        }

        response = requests.get(api_url, headers=headers)
        data = response.json()

        if data.get("results", 0) > 0:
            teams_data = data["response"]

            for team_data in teams_data:
                if team_data.get("nbaFranchise", False) and team_data.get("logo"):
                    team_info = {
                        "team_id": team_data["id"],
                        "name": team_data["name"],
                        "nickname": team_data["nickname"],
                        "code": team_data["code"],
                        "city": team_data["city"],
                        "logo": team_data["logo"],
                        "all_star": team_data["allStar"],
                        "nba_franchise": team_data["nbaFranchise"],
                        "conference": team_data.get("leagues", {}).get("standard", {}).get("conference", ""),
                        "division": team_data.get("leagues", {}).get("standard", {}).get("division", ""),
                    }

                    # Save the team information to the database
                    nba_team, created = Team.objects.update_or_create(team_id=team_info["team_id"], defaults=team_info)

                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Team '{nba_team}' added to the database."))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Team '{nba_team}' updated in the database."))
                else:
                    self.stdout.write(self.style.NOTICE(f"Skipping non-NBA franchise: {team_data['name']}"))
        else:
            self.stdout.write(self.style.ERROR('No team data found in the API response.'))