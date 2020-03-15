from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CreateUserDrinkForm, CreateUserDrinkIngredientForm, CreateUserDrinkInstructionForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from .models import Profile, Drink, DrinkName, ProfileToLikedDrink, ProfileToDislikedDrink, Friend, FriendRequest, UserDrink
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from django.forms.formsets import formset_factory
from .stt import IBM
from gnt.adapters import drink_adapter

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

        discovery_adapter = drink_adapter.DiscoveryAdapter()
        response = discovery_adapter.natural_language_search(text)

        return render(request, 'gnt/results.html', {
            'query': text,
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
    IngredientFormset = formset_factory(CreateUserDrinkIngredientForm)
    InstructionFormset = formset_factory(CreateUserDrinkInstructionForm)

    profile = request.user

    if request.method == 'POST':
        create_user_drink_form = CreateUserDrinkForm(request.POST)

        if create_user_drink_form.is_valid():
            drink = create_user_drink_form.save(commit=False)
            drink.user = request.user
            drink.save()

            ingredient_formset = IngredientFormset(
                request.POST, prefix='ingredient')
            if ingredient_formset.is_valid():
                for ingredient_form in ingredient_formset:
                    ingredient = ingredient_form.save(commit=False)
                    ingredient.drink = drink
                    ingredient.save()

            instruction_formset = InstructionFormset(
                request.POST, prefix='instruction')
            if instruction_formset.is_valid():
                for instruction_form in instruction_formset:
                    instruction = instruction_form.save(commit=False)
                    instruction.drink = drink
                    instruction.save()

                messages.success(request, f'Your drink has been created')
                return redirect('profile_public', username=request.user.username)
    else:
        create_user_drink_form = CreateUserDrinkForm()
        ingredient_formset = IngredientFormset(prefix='ingredient')
        instruction_formset = InstructionFormset(prefix='instruction')

    context = {
        'profile': profile,
        'create_user_drink_form': create_user_drink_form,
        'ingredient_formset': ingredient_formset,
        'instruction_formset': instruction_formset
    }

    return render(request, 'gnt/profile_create_drink.html', context)


@login_required
def profile_edit(request):
    username = User.objects.get(username=request.user)
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile_public', username=request.user.username)
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'profile': username,
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'gnt/profile_edit.html', context)


def profile_public(request, username):
    username = User.objects.get(username=username)
    drinks = UserDrink.objects.filter(user=username).order_by('-timestamp')
    requests = (FriendRequest.objects.filter(requestee=request.user.profile) | FriendRequest.objects.filter(requestor=request.user.profile)) & (
        FriendRequest.objects.filter(requestee=username.profile) | FriendRequest.objects.filter(requestor=username.profile))
    friends = (Friend.objects.filter(friend1=username.profile) & Friend.objects.filter(friend2=request.user.profile)) | (
        Friend.objects.filter(friend1=request.user.profile) & Friend.objects.filter(friend2=username.profile))

    if request.method == 'POST':
        if 'add-friend' in request.POST:
            friend_request = FriendRequest()
            friend_request.requestee = username.profile
            friend_request.requestor = request.user.profile
            friend_request.save()
        elif 'remove-friend' in request.POST:
            friend = Friend.objects.filter(friend1=request.user.profile, friend2=username.profile) | Friend.objects.filter(
                friend1=username.profile, friend2=request.user.profile)
            friend.delete()

    context = {
        'profile': username,
        'drinks': drinks,
        'requests': requests,
        'friends': friends
    }

    return render(request, 'gnt/profile_public.html', context)


@login_required
def liked_drinks(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        profile_to_drink = ProfileToLikedDrink.objects.filter(
            profile_FK=profile.id)
        if profile_to_drink:
            response = [0 for i in range(len(profile_to_drink))]
            discovery_adapter = drink_adapter.DiscoveryAdapter()
            for i, ptd in enumerate(profile_to_drink):
                drink = Drink.objects.get(id=ptd.drink_FK.id)
                obj = discovery_adapter.get_drink(drink.drink_hash)
                response[i] = obj[0]

            context = {
                'profile': user,
                'drinks': response
            }
            return render(request, 'gnt/liked_drinks.html', context)
        else:
            context = {
                'profile': user
            }
            return render(request, 'gnt/liked_drinks.html', context)
    else:
        return HttpResponseRedirect('/home/')


def about(request):
    return render(request, 'gnt/about.html')


def disliked_drinks(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        profile_to_drink = ProfileToDislikedDrink.objects.filter(
            profile_FK=profile.id)
        if profile_to_drink:
            response = [0 for i in range(len(profile_to_drink))]
            discovery_adapter = drink_adapter.DiscoveryAdapter()
            for i, ptd in enumerate(profile_to_drink):
                drink = Drink.objects.get(id=ptd.drink_FK.id)
                obj = discovery_adapter.get_drink(drink.drink_hash)
                response[i] = obj[0]
            context = {
                'profile': request.user,
                'drinks': response
            }
            return render(request, 'gnt/disliked_drinks.html', context)
        else:
            context = {
                'profile': request.user
            }
            return render(request, 'gnt/disliked_drinks.html', context)
    else:
        return HttpResponseRedirect('/home/')


def timeline(request):
    drinks = UserDrink.objects.all().order_by('-timestamp')
    context = {
        'drinks': drinks
    }
    return render(request, 'gnt/timeline.html', context)


def search(request):
    if request.method == 'POST':
        profiles = User.objects.filter(
            username__startswith=request.POST['search_input'])
        context = {
            'profiles': profiles
        }
        return render(request, 'gnt/search.html', context)


def notifications(request, username):
    requests = FriendRequest.objects.filter(profile_FK=request.user.profile)

    if 'add-friend' in request.POST:
        requestor = User.objects.get(username=request.POST['requestor'])
        friend_request = FriendRequest.objects.get(
            request_FK=requestor.profile, profile_FK=request.user.profile)
        friend_request.delete()
        friends = Friend()
        friends.profile_FK = request.user.profile
        friends.friend_FK = requestor.profile
        friends.save()

        messages.success(
            request, f'you have successfully added friend { requestor.profile.user }')

    elif 'deny-friend' in request.POST:
        requestor = User.objects.get(username=request.POST['requestor'])
        friend_request = FriendRequest.objects.get(
            request_FK=requestor.profile, profile_FK=request.user.profile)
        friend_request.delete()

        messages.info(
            request, f'you have denied to add friend { requestor.profile.user }')

    context = {
        'requests': requests
    }

    return render(request, 'gnt/notifications.html', context)


@login_required
def friends(request, username):
    if request.method == 'POST':

        if 'add-friend' in request.POST:
            requestor = User.objects.get(username=request.POST['requestor'])
            friend_request = FriendRequest.objects.get(
                requestor=requestor.profile, requestee=request.user.profile)
            friend_request.delete()
            friends = Friend()
            friends.friend1 = request.user.profile
            friends.friend2 = requestor.profile
            friends.save()

            messages.success(
                request, f'you have successfully added friend { requestor.profile.user }')

        elif 'remove-friend' in request.POST:
            requestor = User.objects.get(username=request.POST['requestor'])
            friends = Friend.objects.get(
                friend1=requestor.profile, friend2=request.user.profile)
            friends.delete()

            messages.success(
                request, f'you have removed friend { requestor.profile.user }')

    friends = Friend.objects.filter(friend1=request.user.profile) | Friend.objects.filter(
        friend2=request.user.profile)

    context = {
        'profile': request.user,
        'friends': friends
    }
    return render(request, 'gnt/friends.html', context)
