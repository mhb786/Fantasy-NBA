from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from mysite.models import Team, NBAPlayer, User
from mysite.views import team_profile, merge_sort
from django.contrib.auth.models import AnonymousUser


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.team = Team.objects.create(team_id=1, name="Lakers")
        self.nba_player = NBAPlayer.objects.create(
            first_name="LeBron",
            last_name="James",
            team="Lakers",
            PPG=25.2,
            APG=10.3,
            RPG=7.4,
            SPG=1.2,
            BPG=0.6,
            FG_PCT=0.510,
            FG3_PCT=0.340,
            FT_PCT=0.730,
            MIN=34.2,
            TOV=3.7
        )
        self.url = reverse('team_profile', kwargs={'team_id': self.team.team_id})
        self.api_key = "1653a1f50amsha7a04d5574bda05p123149jsn718df4a7a999"
        self.fixtures_url = reverse('fixtures')
        self.client.login(username='testuser', password='12345')  # Ensure user is logged in

    @patch('mysite.views.get_stats')
    @patch('mysite.views.NBAPlayer.objects.filter')
    def test_team_profile_view(self, mock_filter, mock_get_stats):
        # Mock setups
        mock_filter.return_value = [self.nba_player]
        mock_get_stats.return_value = [25, 10, 5, 3, 1, 2, 0.5, 0.8, 0.9, 1, 0.45]

        # Make request to the view
        response = self.client.get(self.url)

        # Check response code and other expectations
        self.assertEqual(response.status_code, 200)
        self.assertIn('team', response.context)
        self.assertEqual(response.context['team'], self.team)

        players_with_stats = response.context['players_with_stats']
        self.assertIsInstance(players_with_stats, list)
        self.assertEqual(len(players_with_stats), 1)
        expected_stats = {
            'first_name': 'LeBron',
            'last_name': 'James',
            'stats': [25, 10, 5, 3, 1, 2, 0.5, 0.8, 0.9, 1, 0.45]
        }
        self.assertDictEqual(players_with_stats[0], expected_stats)

    
    def test_merge_sort_function(self):
        # List of article titles in non-sorted order
        titles = ["NBA Finals Update", "LeBron Leads the Game", "Sports Today"]
        
        # Expected sorted list
        expected_sorted_titles = ["LeBron Leads the Game", "NBA Finals Update", "Sports Today"]

        # Apply the merge_sort function to the titles
        sorted_titles = merge_sort(titles)

        # Assert that the sorted titles match the expected order
        self.assertEqual(sorted_titles, expected_sorted_titles)

    @patch('requests.get')
    def test_get_fixtures_for_date(self, mock_get):
        # Setup mock
        mock_response = MagicMock()
        expected_data = {'response': [{'game_id': '123', 'team_home': 'Team A', 'team_away': 'Team B'}]}
        mock_response.json.return_value = expected_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        from mysite.views import get_fixtures_for_date
        result = get_fixtures_for_date(self.api_key, '2021-03-10')

        # Asserts
        self.assertEqual(result, expected_data['response'])
        mock_get.assert_called_once_with(
            "https://api-nba-v1.p.rapidapi.com/games",
            headers={
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com"
            },
            params={"date": '2021-03-10'}
        )

    @patch('mysite.views.get_fixtures_for_date')
    def test_fixtures_view(self, mock_get_fixtures):
        # Setup mock
        mock_get_fixtures.return_value = [{'game_id': '123', 'team_home': 'Team A', 'team_away': 'Team B'}]
        response = self.client.post(self.fixtures_url, {'date': '2021-03-10'})

        # Verify
        self.assertEqual(response.status_code, 200)
        mock_get_fixtures.assert_called_once_with(self.api_key, '2021-03-10')
        self.assertTemplateUsed(response, 'mysite/fixtures.html')
        self.assertIn('fixtures', response.context)
        self.assertIn('specific_date', response.context)
        self.assertEqual(response.context['specific_date'], '2021-03-10')