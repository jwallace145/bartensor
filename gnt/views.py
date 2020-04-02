"""
Views Module
"""

# import necessary modules
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from gnt.adapters import drink_adapter
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, CreateUserDrinkForm, CreateUserDrinkIngredientForm, CreateUserDrinkInstructionForm
from .models import Profile, Drink, ProfileToLikedDrink, ProfileToDislikedDrink, Friend, FriendRequest, UserDrink, UpvotedUserDrink, DownvotedUserDrink
from .stt import IBM


def bad_request(request):
    """
    Bad Request View
    """

    return HttpResponseRedirect(reverse('home'))


def home(request):
    """
    Home View
    """

    return render(request, 'gnt/index.html')


def results(request):
    """
    Results View
    """

    if request.method == 'POST':
        if 'audio' in request.FILES:
            audio = request.FILES['audio']
            text = IBM().transcribe(audio)
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


def more_results(request):
    """
    More results with an offset
    """
    text = request.POST['text']
    offset = request.POST['offset']
    discovery_adapter = drink_adapter.DiscoveryAdapter()
    response = discovery_adapter.natural_language_search_offset(
        text, offset)
    return render(request, 'gnt/drink_results_with_voting.html', {
        'query': text,
        'drinks': response
    })


def register(request):
    """
    Register View
    """

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request, f'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }

    return render(request, 'gnt/register.html', context)


@login_required
def profile_create_drink(request, username):
    """
    Profile Create Drink View
    """

    username = User.objects.get(username=username)

    IngredientFormset = formset_factory(CreateUserDrinkIngredientForm)
    InstructionFormset = formset_factory(CreateUserDrinkInstructionForm)

    if request.method == 'POST':
        create_user_drink_form = CreateUserDrinkForm(request.POST)
        print(request.POST)

        if create_user_drink_form.is_valid():
            drink = create_user_drink_form.save(commit=False)
            drink.user = request.user
            drink.likes = 0
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

                messages.success(
                    request, f'Your drink { drink.name } has been created!')
                return redirect('profile_public', username=request.user.username)
    else:
        create_user_drink_form = CreateUserDrinkForm()
        ingredient_formset = IngredientFormset(prefix='ingredient')
        instruction_formset = InstructionFormset(prefix='instruction')

    context = {
        'profile': username,
        'create_user_drink_form': create_user_drink_form,
        'ingredient_formset': ingredient_formset,
        'instruction_formset': instruction_formset
    }

    return render(request, 'gnt/profile_create_drink.html', context)


@login_required
def profile_edit(request, username):
    """
    Profile Edit View
    """

    username = User.objects.get(username=username)
    profile = Profile.objects.get(user=username)

    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=username)
        profile_update_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile_public', username=request.user.username)
    else:
        user_update_form = UserUpdateForm(instance=username)
        profile_update_form = ProfileUpdateForm(instance=profile)

    context = {
        'profile': username,
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'gnt/profile_edit.html', context)


def profile_public(request, username):
    """
    Profile View
    """
    username = User.objects.get(username=username)
    drinks = UserDrink.objects.filter(user=username).order_by('-timestamp')
    if request.user.is_authenticated:
        requests = (FriendRequest.objects.filter(requestee=request.user.profile) | FriendRequest.objects.filter(requestor=request.user.profile)) & (
            FriendRequest.objects.filter(requestee=username.profile) | FriendRequest.objects.filter(requestor=username.profile))
        friends = (Friend.objects.filter(friend1=username.profile) & Friend.objects.filter(friend2=request.user.profile)) | (
            Friend.objects.filter(friend1=request.user.profile) & Friend.objects.filter(friend2=username.profile))
    else:
        requests = []
        friends = []

    if request.method == 'POST':
        if 'add-friend' in request.POST:
            friend_request = FriendRequest()
            friend_request.requestee = username.profile
            friend_request.requestor = request.user.profile
            friend_request.save()

            messages.success(request, f'Friend request sent to { username }!')
        elif 'remove-friend' in request.POST:
            friend = Friend.objects.filter(friend1=request.user.profile, friend2=username.profile) | Friend.objects.filter(
                friend1=username.profile, friend2=request.user.profile)
            friend.delete()

            messages.info(request, f'Removed friend { username }!')

        elif 'like-drink' in request.POST:
            drink = UserDrink.objects.get(name=request.POST['drink'])
            profile = request.user.profile
            # if LikeUserDrink.objects.filter(drink=drink, profile=profile).count() == 0:
            #     drink.likes += 1
            #     drink.save()
            #     like = LikeUserDrink(drink=drink, profile=profile)
            #     like.save()

    context = {
        'profile': username,
        'drinks': drinks,
        'requests': requests,
        'friends': friends,
    }

    return render(request, 'gnt/profile_public.html', context)


def liked_drinks(request, username):
    """
    Liked Drinks View
    """

    username = User.objects.get(username=username)
    profile = Profile.objects.get(user=username)

    profile_to_drink = ProfileToLikedDrink.objects.filter(profile=profile.id)

    if profile_to_drink:
        response = [0 for i in range(len(profile_to_drink))]

        discovery_adapter = drink_adapter.DiscoveryAdapter()

        for i, ptd in enumerate(profile_to_drink):
            drink = Drink.objects.get(id=ptd.drink.id)
            obj = discovery_adapter.get_drink(drink.drink_hash)
            response[i] = obj[0]

        context = {
            'profile': username,
            'drinks': response
        }

        return render(request, 'gnt/liked_drinks.html', context)
    else:
        context = {
            'profile': username
        }

        return render(request, 'gnt/liked_drinks.html', context)


def about(request):
    """
    About View
    """

    return render(request, 'gnt/about.html')


def disliked_drinks(request, username):
    """
    Disliked Drinks View
    """

    username = User.objects.get(username=username)
    profile = Profile.objects.get(user=username)

    profile_to_drink = ProfileToDislikedDrink.objects.filter(
        profile=profile.id)

    if profile_to_drink:
        response = [0 for i in range(len(profile_to_drink))]

        discovery_adapter = drink_adapter.DiscoveryAdapter()

        for i, ptd in enumerate(profile_to_drink):
            drink = Drink.objects.get(id=ptd.drink.id)
            obj = discovery_adapter.get_drink(drink.drink_hash)
            response[i] = obj[0]

        context = {
            'profile': username,
            'drinks': response
        }

        return render(request, 'gnt/disliked_drinks.html', context)
    else:
        context = {
            'profile': username
        }

        return render(request, 'gnt/disliked_drinks.html', context)


def timeline_pop(request):
    """
    Timeline View
    """

    drinks = UserDrink.objects.all().order_by('-votes')

    context = {
        'drinks': drinks
    }

    return render(request, 'gnt/timeline.html', context)


def timeline(request):
    """
    Timeline View
    """

    drinks = UserDrink.objects.all().order_by('-timestamp')

    context = {
        'drinks': drinks
    }

    return render(request, 'gnt/timeline.html', context)


def search(request):
    """
    Search View
    """

    if request.method == 'POST':
        profiles = User.objects.filter(
            username__startswith=request.POST['search_input'])

        context = {
            'profiles': profiles
        }

        return render(request, 'gnt/search.html', context)


def notifications(request, username):
    """
    Notifications View
    """

    requests = FriendRequest.objects.filter(requestee=request.user.profile)

    if request.method == 'POST':
        if 'add-friend' in request.POST:
            requestor = User.objects.get(username=request.POST['requestor'])
            friend_request = FriendRequest.objects.get(
                requestee=request.user.profile, requestor=requestor.profile)
            friend_request.delete()
            friends = Friend(friend1=request.user.profile,
                             friend2=requestor.profile)
            friends.save()

            messages.success(
                request, f'You have added friend { requestor.profile.user }!')

        elif 'deny-friend' in request.POST:
            requestor = User.objects.get(username=request.POST['requestor'])
            friend_request = FriendRequest.objects.get(
                requestee=request.user.profile, requestor=requestor.profile)
            friend_request.delete()

            messages.info(
                request, f'you have denied to add friend { requestor.profile.user }')

    context = {
        'requests': requests
    }

    return render(request, 'gnt/notifications.html', context)


def friends(request, username):
    """
    Friends View
    """

    username = User.objects.get(username=username)
    profile = Profile.objects.get(user=username)

    if request.method == 'POST':
        if 'remove-friend' in request.POST:
            requestor = User.objects.get(username=request.POST['requestor'])
            friends = Friend.objects.filter(friend1=requestor.profile, friend2=request.user.profile) | Friend.objects.filter(
                friend1=request.user.profile, friend2=requestor.profile)
            friends.delete()

            messages.success(
                request, f'you have removed friend { requestor.profile.user }')

    friends = Friend.objects.filter(friend1=profile) | Friend.objects.filter(
        friend2=profile)

    context = {
        'profile': username,
        'friends': friends
    }

    return render(request, 'gnt/friends.html', context)
