from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'gnt/index.html')

def signup(request):
    if request.method == 'POST':
        # TODO: Fill in correct url for redirect
        return redirect('/')
    else:
        return render(request, 'gnt/signup.html')

def login(request):
    if request.method == 'POST':
        # TODO: Fill in correct url for redirect
        return redirect('/')
    else:
        return render(request, 'gnt/login.html')

def results(request):
    return render(request, 'gnt/results.html')

def loading(request):
    return render(request, 'gnt/loading.html')