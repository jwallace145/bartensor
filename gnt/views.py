from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User

def index(request):
    logged_in = len(User.objects.filter(username='big_duddy666')) > 0
    for user in User.objects.all():
        user.delete()
    return render(request, 'gnt/index.html', {
            'logged_in': logged_in,
        })

def signup(request):
    u = User(username='big_duddy666')
    u.save()
    if request.method == 'POST':
        # TODO sign up user here
        return HttpResponseRedirect(reverse('gnt:index'))
    else:
        return render(request, 'gnt/signup.html')

def login(request):
    u = User(username='big_duddy666')
    u.save()
    if request.method == 'POST':
        # TODO: login user here
        return HttpResponseRedirect(reverse('gnt:index'))
    else:
        return render(request, 'gnt/login.html')

def results(request):
    return render(request, 'gnt/results.html')