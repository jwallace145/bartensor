from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'gnt/index.html')

def signup(request):
    return render(request, 'gnt/signup.html')

def login(request):
    return render(request, 'gnt/login.html')