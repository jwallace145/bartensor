from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CreateUserDrinkForm, CreateUserDrinkIngredientForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from .models import Profile, Drinks, Drink_names, Profile_to_liked_drink, Profile_to_disliked_drink, Friend, Friend_request
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from .stt import IBM

# get api key from settings.py which is stored as an environment variable
api_key = getattr(settings, 'WATSON_DISCOVERY_API_KEY', None)

def bad_request(request, *args, **kwargs):
    return HttpResponseRedirect(reverse('home'))


def home(request):
    return render(request, 'gnt/index.html')


def results(request):
    if request.method == 'POST':
        if 'audio' in request.FILES:
            audio = request.FILES['audio']
            text = IBM().transcribe(audio)
            print(text)
        else:
            text = request.POST['search_bar']

        environment_id = 'b7d1486c-2fdc-40c5-a2ce-2d78ec48fa76'
        collection_id = '7c11f329-5f31-4e59-aa63-fde1e91ff681'

        authenticator = IAMAuthenticator(api_key)
        discovery = DiscoveryV1(
            version='2019-04-30',
            authenticator=authenticator
        )
        discovery.set_service_url(
            'https://api.us-south.discovery.watson.cloud.ibm.com/')

        response = discovery.query(
            environment_id, collection_id, natural_language_query=text).result['results']

        return render(request, 'gnt/results.html', {
            'drinks': response
        })
    else:
        return HttpResponseRedirect(reverse('home'))


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
def profile_create_drink(request):
    if request.method == 'POST':
        profile = Profile.objects.get(id=request.user.profile.id)

        create_user_drink_form = CreateUserDrinkForm(request.POST)
        if create_user_drink_form.is_valid():
            user_drink = create_user_drink_form.save()
            user_drink.profile_FK = profile
            user_drink.save()

            create_user_drink_ingredient_form = CreateUserDrinkIngredientForm(
                request.POST)

            if create_user_drink_ingredient_form.is_valid():
                user_drink_ingredient = create_user_drink_ingredient_form.save()
                user_drink_ingredient.user_drink_FK = user_drink
                user_drink_ingredient.save()

                messages.success(request, f'Your drink has been created')
                return redirect('profile_public')
    else:
        create_user_drink_form = CreateUserDrinkForm()
        create_user_drink_ingredient_form = CreateUserDrinkIngredientForm()

    context = {
        'create_user_drink_form': create_user_drink_form,
        'create_user_drink_ingredient_form': create_user_drink_ingredient_form
    }
    return render(request, 'gnt/profile_create_drink.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(
                request, f'Your account has been updated!')
            return redirect('profile_public')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'gnt/profile_edit.html', context)


@login_required
def profile_public(request):
    return render(request, 'gnt/profile_public.html')

def get_liked_disliked_drinks(request):
    try:
        environment_id = 'b7d1486c-2fdc-40c5-a2ce-2d78ec48fa76'
        collection_id = '7c11f329-5f31-4e59-aa63-fde1e91ff681'

        authenticator = IAMAuthenticator(api_key)
        discovery = DiscoveryV1(
            version='2019-04-30',
            authenticator=authenticator
        )
        liked_drinks = []
        disliked_drinks = []
        user = request.user
        profile = Profile.objects.get(user=user)
        # get liked drinks
        profile_to_liked_drink = Profile_to_liked_drink.objects.filter(profile_FK=profile.id)
        if profile_to_liked_drink:
            response = [0 for i in range(len(profile_to_liked_drink))]
            for i, ptd in enumerate(profile_to_liked_drink):
                response[i] = ptd.drink_FK.drink_hash
            liked_drinks = response
        # get disliked drinks
        profile_to_disliked_drink = Profile_to_disliked_drink.objects.filter(profile_FK=profile.id)
        if profile_to_disliked_drink:
            response = [0 for i in range(len(profile_to_disliked_drink))]
            for i, ptd in enumerate(profile_to_disliked_drink):
                response[i] = ptd.drink_FK.drink_hash
            disliked_drinks = response
        # return response
        resp = {
            'message': [liked_drinks, disliked_drinks],
            'status': 201
        }    
        return JsonResponse(resp)
    except Exception as e:
        print(str(e))
        response = {
            'message': str(e),
            'status': 500
        }
        return JsonResponse(response)


def liked_drinks(request):
    if request.user.is_authenticated:
        environment_id = 'b7d1486c-2fdc-40c5-a2ce-2d78ec48fa76'
        collection_id = '7c11f329-5f31-4e59-aa63-fde1e91ff681'

        authenticator = IAMAuthenticator(api_key)
        discovery = DiscoveryV1(
            version='2019-04-30',
            authenticator=authenticator
        )
        discovery.set_service_url(
            'https://api.us-south.discovery.watson.cloud.ibm.com/')

        user = request.user
        profile = Profile.objects.get(user=user)
        profile_to_drink = Profile_to_liked_drink.objects.filter(
            profile_FK=profile.id)
        if profile_to_drink:
            response = [0 for i in range(len(profile_to_drink))]
            for i, ptd in enumerate(profile_to_drink):
                drink = Drinks.objects.get(id=ptd.drink_FK.id)
                obj = discovery.query(
                    environment_id, collection_id, query=f'id::"{drink.drink_hash}"').result['results']
                response[i] = obj[0]
            return render(request, 'gnt/liked_drinks.html', {
                'drinks': response
            })
        else:
            return render(request, 'gnt/liked_drinks.html')
    else:
        return HttpResponseRedirect('/home/')


def about(request):
    return render(request, 'gnt/about.html')


def like_drink(request):
    try:
        username = request.POST['user']
        drink = Drinks.objects.get(drink_hash=request.POST['drink_id'])
        
        profile = Profile.objects.get(id=request.user.profile.id)
        # Check to see if drink is disliked then remove
        disliked_drink = Profile_to_disliked_drink.objects.filter(
            profile_FK=profile, drink_FK=drink)
        if disliked_drink:
            disliked_drink.delete()

        if Profile_to_liked_drink.objects.filter(profile_FK=profile, drink_FK=drink):
            response = {
                'message': "Drink " + str(request.POST['drink_id']) + " has already been liked by " + str(username) + ". No changes to db",
                'status': 422
            }
        else:
            new_like = Profile_to_liked_drink(
                profile_FK=profile, drink_FK=drink)
            new_like.save()
            msg = "Drink " + \
                str(request.POST['drink_id']) + "added to " + \
                str(username) + "'s liked drinks"
            response = {
                'message': msg,
                'status': 201
            }
        return JsonResponse(response)
    except Exception as e:
        print(str(e))
        response = {
            'message': str(e),
            'status': 500
        }
        return JsonResponse(response)


def dislike_drink(request):
    try:
        username = request.POST['user']
        drink = Drinks.objects.get(drink_hash=request.POST['drink_id'])
        profile = Profile.objects.get(id=request.user.profile.id)
        # If user has liked drink, remove it from liked table
        liked_drink = Profile_to_liked_drink.objects.filter(
            profile_FK=profile, drink_FK=drink)
        if liked_drink:
            # Remove liked drink
            liked_drink.delete()

        if Profile_to_disliked_drink.objects.filter(profile_FK=profile, drink_FK=drink):
            response = {
                'message': "Drink " + str(request.POST['drink_id']) + " has already been disliked by " + str(username) + ". No changes to db",
                'status': 422
            }
        else:
            new_dislike = Profile_to_disliked_drink(
                profile_FK=profile, drink_FK=drink)
            new_dislike.save()
            msg = "Drink " + \
                str(request.POST['drink_id']) + "added to " + \
                str(username) + "'s disliked drinks"
            response = {
                'message': msg,
                'status': 201
            }
        return JsonResponse(response)
    except Exception as e:
        print(str(e))
        response = {
            'message': str(e),
            'status': 500
        }
        return JsonResponse(response)


def remove_liked_drink(request):
    try:
        username = request.POST['user']
        drink = Drinks.objects.get(drink_hash=request.POST['drink_id'])
        profile = Profile.objects.get(id=request.user.profile.id)
        liked_drink = Profile_to_liked_drink.objects.filter(
            profile_FK=profile, drink_FK=drink)
        if liked_drink:
            liked_drink.delete()
            response = {
                'message': "Drink " + str(request.POST['drink_id']) + " deleted for ",
                'status': 200
            }
        else:
            response = {
                'message': 'Drink ' + str(drink) + ' not liked for ' + str(username),
                'status': 404
            }
        return JsonResponse(response)
    except Exception as e:
        print(str(e))
        response = {
            'message': str(e),
            'status': 500
        }
        return JsonResponse(response)

def disliked_drinks(request):
    if request.user.is_authenticated:
        environment_id = 'b7d1486c-2fdc-40c5-a2ce-2d78ec48fa76'
        collection_id = '7c11f329-5f31-4e59-aa63-fde1e91ff681'

        authenticator = IAMAuthenticator(api_key)
        discovery = DiscoveryV1(
            version='2019-04-30',
            authenticator=authenticator
        )
        discovery.set_service_url(
            'https://api.us-south.discovery.watson.cloud.ibm.com/')

        user = request.user
        profile = Profile.objects.get(user=user)
        profile_to_drink = Profile_to_disliked_drink.objects.filter(
            profile_FK=profile.id)
        if profile_to_drink:
            response = [0 for i in range(len(profile_to_drink))]
            for i, ptd in enumerate(profile_to_drink):
                drink = Drinks.objects.get(id=ptd.drink_FK.id)
                obj = discovery.query(
                    environment_id, collection_id, query=f'id::"{drink.drink_hash}"').result['results']
                response[i] = obj[0]
            return render(request, 'gnt/disliked_drinks.html', {
                'drinks': response
            })
        else:
            return render(request, 'gnt/disliked_drinks.html')
    else:
        return HttpResponseRedirect('/home/')

def remove_disliked_drink(request):
    try:
        username = request.POST['user']
        drink = Drinks.objects.get(drink_hash=request.POST['drink_id'])
        profile = Profile.objects.get(id=request.user.profile.id)
        disliked_drink = Profile_to_disliked_drink.objects.filter(profile_FK=profile, drink_FK=drink)
        if disliked_drink:
            disliked_drink.delete()
            response = {
                'message': "Drink " + str(request.POST['drink_id']) + " deleted for ",
                'status': 200
            }
        else:
            response = {
                'message': 'Drink ' + str(drink) + ' not disliked for ' + str(username),
                'status': 404
            }
        return JsonResponse(response)
    except Exception as e:
        print(str(e))
        response = {
            'message': str(e),
            'status': 500
        }
        return JsonResponse(response)
