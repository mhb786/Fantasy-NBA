from django.shortcuts import render
from django.http import HttpResponse
from .models import NBAPlayer

# Create your views here.

def home(response):
    return render(response, "mysite/home.html", {})