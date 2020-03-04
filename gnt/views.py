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

# get api key from settings.py which is stored as an environment variable
api_key = getattr(settings, 'WATSON_DISCOVERY_API_KEY', None)


def bad_request(request, *args, **kwargs):
    return HttpResponseRedirect('/home/')


def home(request):
    return render(request, 'gnt/index.html')


def results(request):

    if request.method == 'POST':
        environment_id = 'b7d1486c-2fdc-40c5-a2ce-2d78ec48fa76'
        collection_id = '7c11f329-5f31-4e59-aa63-fde1e91ff681'

        authenticator = IAMAuthenticator(api_key)
        discovery = DiscoveryV1(
            version='2019-04-30',
            authenticator=authenticator
        )
        discovery.set_service_url(
            'https://api.us-south.discovery.watson.cloud.ibm.com/')

        text = request.POST['search_bar']
        response = discovery.query(
            environment_id, collection_id, natural_language_query=text).result['results']

        return render(request, 'gnt/results.html', {
            'drinks': response
        })
    else:
        return HttpResponseRedirect(reverse('home'))


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
