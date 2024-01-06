# forms.py
from django import forms
from .models import NBAPlayer

class PlayerComparisonForm(forms.Form):
    player1 = forms.ModelChoiceField(queryset=NBAPlayer.objects.all(), label='Player 1')
    player2 = forms.ModelChoiceField(queryset=NBAPlayer.objects.all(), label='Player 2')

class DateSelectionForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))