# forms.py
from django import forms
from .models import NBAPlayer

class PlayerComparisonForm(forms.Form):
    player1 = forms.ModelChoiceField(queryset=NBAPlayer.objects.all(), label='Select Player 1')
    player2 = forms.ModelChoiceField(queryset=NBAPlayer.objects.all(), label='Select Player 2')

    # Use the correct keys from the API response
    stats = ['GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT',
             'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST',
             'STL', 'BLK', 'TOV', 'PF', 'PTS']
    
    selected_stats = forms.MultipleChoiceField(choices=[(stat, stat) for stat in stats],
                                               widget=forms.CheckboxSelectMultiple,
                                               required=True)

class DateSelectionForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class NBAStatsForm(forms.Form):
    SEASON_CHOICES = [
        ("2023-24", "2023-24"),
        ("2022-23", "2022-23"),
        ("2021-22", "2021-22"),
        ("2020-21", "2020-21"),
        ("2019-20", "2019-20")
    ]

    STAT_CATEGORY_CHOICES = [
        ("PTS", "Points"),
        ("REB", "Rebounds"),
        ("GP", "Games Played"),
        ("MIN", "Minutes Per Game"),
        ("FGM", "Field Goals Made"),
        ("FGA", "Field Goals Attempted"),
        ("FG_PCT", "Field Goal Percentage"),
        ("FG3M", "Three-Pointers Made"),
        ("FG3A", "Three-Pointers Attempted"),
        ("FG3_PCT", "Three-Point Percentage"),
        ("FTM", "Free Throws Made"),
        ("FTA", "Free Throws Attempted"),
        ("FT_PCT", "Free Throw Percentage"),
        ("OREB", "Offensive Rebounds"),
        ("DREB", "Defensive Rebounds"),
        ("REB", "Total Rebounds"),
        ("AST", "Assists"),
        ("STL", "Steals"),
        ("BLK", "Blocks"),
        ("TOV", "Turnovers"),
        ("PF", "Personal Fouls"),
        ("EFF", "Efficiency"),
        ("AST_TOV", "Assist to Turnover Ratio"),
        ("STL_TOV", "Steal to Turnover Ratio"),
    ]

    season = forms.ChoiceField(choices=SEASON_CHOICES)
    stat_category = forms.ChoiceField(choices=STAT_CATEGORY_CHOICES)


from .models import Thread, Post

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']


from .models import Profile

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']