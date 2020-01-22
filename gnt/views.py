from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'gnt/index.html')

def signup(request):
    return HttpResponse('Sign up stub')

def login(request):
    return HttpResponse('Login stub')
