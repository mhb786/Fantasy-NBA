from django.core.management.base import BaseCommand
from mysite.models import Fixture
import requests, time
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Populate the NBAFixture model with fixture data'

    def handle(self, *args, **options):
        url = "https://api-nba-v1.p.rapidapi.com/games"

        start_date = datetime(2023, 10, 24)
        end_date = datetime(2024, 4, 20)

        current_date = start_date

        headers = {
            "X-RapidAPI-Key": "1653a1f50amsha7a04d5574bda05p123149jsn718df4a7a999",
            "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
        }
        while current_date <= end_date:
            formatted_date = current_date.strftime('%Y-%m-%d')
            query_params = {'date': formatted_date}
            games_data = requests.get(url, headers=headers, params=query_params)
            games_data.raise_for_status()

            for game in games_data.json()['response']:
                gamedate=game['date']['start'][:10]
                gametime=game['date']['start'].split('T')[1][:5]
                hometeam=game['teams']['home']['name']
                awayteam=game['teams']['visitors']['name']
                hometeamscore=game['scores']['home']['points']
                awayteamscore=game['scores']['visitors']['points']
                hometeam_logo=game['teams']['home']['logo']
                awayteam_logo=game['teams']['visitors']['logo']

            Fixture.objects.create(gamedate=gamedate, gametime=gametime, hometeam=hometeam, awayteam=awayteam, hometeamscore=hometeamscore, awayteamscore=awayteamscore, hometeam_logo=hometeam_logo, awayteam_logo=awayteam_logo)

            current_date += timedelta(days=1)