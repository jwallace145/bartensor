from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect



# Handles all non specified urls that we don't want users seeing
def bad_request(request, *args, **kwargs):
    return HttpResponseRedirect('/home/')


def home(request):
    return render(request, 'gnt/index.html')


def results(request):
    # TODO: Replace hard coded drinks with information passed into request
    drinks = [
        {
            'id': 'ankeoigab4a34q35htrgif847qyrahd',
            'picture': 'https://assets.bonappetit.com/photos/57acc14e53e63daf11a4d9b6/master/pass/whiskey-sour.jpg',
            'name': 'Whiskey Sour',
                    'ingredients': ['1 ½ oz oz Whiskey',
                                    '2 oz Sour Mix (Fresh preferred)',
                                    'Optional: 1/2 oz egg white (makes drink foamy)'
                                    ],
                    'method': ['glass: Highball',
                               'Shake Ingredients in a Mixing Glass or Cocktail Shaker w/ice',
                               'Strain into a large old fashioned glass with fresh ice',
                               'Garnish with cherry & orange'
                               ]

        },
        {
            'id': '394agdnavior;oa4eih',
            'picture': 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcS9h-WqGmZDxZTkvjEqRWyDG0ZIw5wC6RlQyFj_THX8fmYcQEgv',
            'name': 'Old Fashioned',
                    'ingredients': ['Packet of Sugar',
                                    '2 dashes of Bitters',
                                    'Splash of soda',
                                    'Cherry & orange',
                                    '2 oz Whiskey'
                                    ],
                    'method': [	'glass: Rocks glass',
                                'Muddle sugar, bitters, soda in glass',
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
    return render(request, 'gnt/loading.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'gnt/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(
                request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'gnt/profile.html', context)
