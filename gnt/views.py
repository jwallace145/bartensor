from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Drinks, Drink_names, Profile_to_drink
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def bad_request(request, *args, **kwargs):
    return HttpResponseRedirect('/home/')


def home(request):
    return render(request, 'gnt/index.html')


def results(request):
    if request.method == 'POST':
        environment_id = 'b7d1486c-2fdc-40c5-a2ce-2d78ec48fa76'
        collection_id = '7c11f329-5f31-4e59-aa63-fde1e91ff681'

        authenticator = IAMAuthenticator(
            'Jc1KWt03zHYFzwvVf3_UVOyFpdagyO7P8GU-9ra9_8cy')
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


def liked_drinks(request):
    if request.user.is_authenticated:
        environment_id = 'b7d1486c-2fdc-40c5-a2ce-2d78ec48fa76'
        collection_id = '7c11f329-5f31-4e59-aa63-fde1e91ff681'

        authenticator = IAMAuthenticator(
            'Jc1KWt03zHYFzwvVf3_UVOyFpdagyO7P8GU-9ra9_8cy')
        discovery = DiscoveryV1(
            version='2019-04-30',
            authenticator=authenticator
        )
        discovery.set_service_url(
            'https://api.us-south.discovery.watson.cloud.ibm.com/')

        user = request.user
        profile = Profile.objects.get(user=user)
        profile_to_drink = Profile_to_drink.objects.filter(profile_FK=profile.id)
        if profile_to_drink:
            response = [0 for i in range(len(profile_to_drink))]
            for i, ptd in enumerate(profile_to_drink):
                drink = Drinks.objects.get(id=ptd.drink_FK.id)
                obj = discovery.query(environment_id, collection_id, query=f'id::"{drink.drink_hash}"').result['results']
                response[i] = obj[0]
            return render(request, 'gnt/liked_drinks.html', {
                'drinks': response
            })
        else:
            return render(request, 'gnt/liked_drinks.html')
    else:
        return HttpResponseRedirect('/home/')
