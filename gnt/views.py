from django.shortcuts import render

def index(request):
    return render(request, 'gnt/index.html')