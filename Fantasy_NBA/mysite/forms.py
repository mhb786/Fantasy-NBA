# forms.py
from django import forms
from .models import NBAPlayer

class PlayerComparisonForm(forms.Form):
    player1 = forms.ModelChoiceField(queryset=NBAPlayer.objects.all(), label='Player 1')
    player2 = forms.ModelChoiceField(queryset=NBAPlayer.objects.all(), label='Player 2')

class DateSelectionForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class SeasonForm(forms.Form):
    SEASON_CHOICES = [
        ('2022-23', '2023-24'),
        # Add other season choices as needed
    ]

    selected_season = forms.ChoiceField(choices=SEASON_CHOICES, label='Select Season')