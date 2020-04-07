"""
Views Module
"""

from string import punctuation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from gnt.adapters import drink_adapter
from gnt.adapters.stt_adapter import IBM
from nltk.tokenize.treebank import TreebankWordTokenizer

from .forms import (CreateCommentForm, CreateUserDrinkForm,
                    CreateUserDrinkIngredientForm,
                    CreateUserDrinkInstructionForm, ProfileUpdateForm,
                    UserRegisterForm, UserUpdateForm)
from .models import (Comment, Drink, Friend, FriendRequest, Profile,
                     ProfileToDislikedDrink, ProfileToLikedDrink,
                     UpvotedUserDrink, UserDrink)


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

        positive = ''  # DQL for checking drink names/ingredients might include certain words
        negative = ''  # DQL for ensuring drink ingredients exclude certain words
        # stopwords copied from nltk.corpus.stopwords.words('english')
        stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
                     "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's",
                     'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs',
                     'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am',
                     'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
                     'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
                     'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
                     'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
                     'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all',
                     'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
                     'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't",
                     'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't",
                     'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't",
                     'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn',
                     "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won',
                     "won't", 'wouldn', "wouldn't"]
        # negation stopwords not from any source, we may need to add to this list as we test
        negation_stopwords = ["n't", 'no', 'not', 'nor', 'none', 'never', 'without']
        # split user input into manageable tokens
        tokens = TreebankWordTokenizer().tokenize(text)  # NLTKWordTokenizer supposed to be "improved", but destructive module not found
        # track if we're in a negation phrase
        negate = False
        for token in tokens:
            if token in negation_stopwords:
                # start negating every word if we hit a negation stopword
                negate = True
            elif token in punctuation:
                # stop negating every word if we hit a punctuation mark
                negate = False
            elif token in stopwords:
                # ignore any standard stopwords
                continue

            if negate:
                negative += ','  # comma means logical AND
                negative += 'ingredients:!"%s"' % token  # ingredients must not include token
            else:
                positive += '|'  # bar means logical OR
                positive += 'names:"%s"^2' % token  # drink names should include token and are twice as important
                positive += '|'
                positive += 'ingredients:"%s"' % token  # drink ingredients should include token
        # ignore the first character of each sub-query because we started building them with either | or ,
        positive = positive[1:]
        negative = negative[1:]
        # only include parts of the query that actually exist
        if len(positive) > 0:
            if len(negative) > 0:
                query = '(%s),(%s)' % (positive, negative)
            else:
                query = positive
        elif len(negative) > 0:
            query = negative
        else:
            query = ''
        discovery_adapter = drink_adapter.DiscoveryAdapter()
        response = discovery_adapter.search(query)

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
        create_user_drink_form = CreateUserDrinkForm(request.POST, request.FILES)

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

                messages.success(
                    request, f'Your drink { drink.name } has been created!')
                return redirect('timeline', username=request.user.username)
        else:
            name = request.POST['name']
            messages.error(
                request, f'We already have a cocktail named {name}!')
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

    Users, unathenticated and authenticated, can view other users' profiles with
    this view function. The profile view will render a list of drinks created by
    the user of the profile.

    Args:
        username (string): the username of the given profile

    Return:
        profile_public (html): profile view of given username
    """

    # get user
    user = User.objects.get(username=username)

    # get drinks ordered by new
    drinks = UserDrink.objects.filter(user=user).order_by('-timestamp')

    # if the user is logged in, check friendship status
    if request.user.is_authenticated:
        requests = FriendRequest.objects.filter(
            requestee=user.profile) | FriendRequest.objects.filter(requestor=user.profile)
        friends = (Friend.objects.filter(friend1=user.profile) & Friend.objects.filter(friend2=request.user.profile)) | (
            Friend.objects.filter(friend1=request.user.profile) & Friend.objects.filter(friend2=user.profile))
    else:
        requests = []
        friends = []

    if request.method == 'POST':
        if 'add-friend' in request.POST:
            friend_request = FriendRequest()
            friend_request.requestee = user.profile
            friend_request.requestor = request.user.profile
            friend_request.save()

            messages.success(request, f'Friend request sent to { username }!')
        elif 'remove-friend' in request.POST:
            friend = Friend.objects.filter(friend1=request.user.profile, friend2=user.profile) | Friend.objects.filter(
                friend1=user.profile, friend2=request.user.profile)
            friend.delete()

            messages.info(request, f'Removed friend { username }!')

        elif 'like-drink' in request.POST:
            drink = UserDrink.objects.get(name=request.POST['drink'])
            profile = request.user.profile

            if UpvotedUserDrink.objects.filter(drink=drink, profile=profile).count() == 0:
                drink.likes += 1
                drink.save()
                like = UpvotedUserDrink(drink=drink, profile=profile)
                like.save()

        elif 'create-comment' in request.POST:
            drink = UserDrink.objects.get(id=request.POST['drink'])
            comment = Comment()
            comment.author = request.user
            comment.comment = request.POST['create-comment']
            comment.drink = drink
            comment.save()

    context = {
        'profile': user,
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

        return render(request, 'gnt/profile_liked_drinks.html', context)
    else:
        context = {
            'profile': username
        }

        return render(request, 'gnt/profile_liked_drinks.html', context)


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

        return render(request, 'gnt/profile_disliked_drinks.html', context)
    else:
        context = {
            'profile': username
        }

        return render(request, 'gnt/profile_disliked_drinks.html', context)


def timeline_pop(request):
    """
    Timeline View
    """
    offset = 0
    if request.GET.get('offset', 0):
        offset = int(request.GET['offset'])
    drinks = UserDrink.objects.all().order_by('-votes')[offset:offset + 50]

    context = {
        'drinks': drinks
    }

    return render(request, 'gnt/timeline.html', context)


def timeline(request):
    """
    Timeline View
    """
    offset = 0
    if request.GET.get('offset', 0) != 0:
        offset = int(request.GET['offset'])
    drinks = UserDrink.objects.all().order_by('-timestamp')[offset:offset + 50]

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

    return render(request, 'gnt/profile_friends.html', context)
