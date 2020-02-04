from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User

def index(request):
	return render(request, 'gnt/index.html', {
			'logged_in': len(User.objects.filter(username='big_duddy666')) > 0,
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

def logout(request):
	for user in User.objects.all():
		user.delete()
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def results(request):
	#TODO: Replace hard coded drinks with information passed into request
	drinks = [
		{
			'id': 'ankeoigab4a34q35htrgif847qyrahd',
			'picture': 'https://assets.bonappetit.com/photos/57acc14e53e63daf11a4d9b6/master/pass/whiskey-sour.jpg',
			'name': 'Whiskey Sour',
			'glass': 'Highball',
			'ingredients': ['1 ½ oz oz Whiskey',
							'2 oz Sour Mix (Fresh preferred)',
							'Optional: 1/2 oz egg white (makes drink foamy)'
							],
			'method': ['Shake Ingredients in a Mixing Glass or Cocktail Shaker w/ice',
						'Strain into a large old fashioned glass with fresh ice',
						'Garnish with cherry & orange'
						]

		},
		{
			'id': '394agdnavior;oa4eih',
			'picture': 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcS9h-WqGmZDxZTkvjEqRWyDG0ZIw5wC6RlQyFj_THX8fmYcQEgv',
			'name': 'Old Fashioned',
			'glass': 'Rocks glass',
			'ingredients': ['Packet of Sugar', 
							'2 dashes of Bitters', 
							'Splash of soda',
							'Cherry & orange',
							'2 oz Whiskey'
							],
			'method': ['Muddle sugar, bitters, soda in glass',
						'Add Whiskey',
						'Fill glass with ice'
						]
		}
	]
	context = {
		'drinks': drinks
	}
	return render(request, 'gnt/results.html', context)

def loading(request):
	return render(request, 'gnt/loading.html', {
			'logged_in': len(User.objects.filter(username='big_duddy666')) > 0,
		})
