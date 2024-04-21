from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect("/")
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {'form':form})

