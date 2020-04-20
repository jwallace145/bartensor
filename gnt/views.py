"""
Views Module
"""
from string import punctuation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
import concurrent.futures
from gnt.adapters import drink_adapter
from gnt.adapters.stt_adapter import IBM
from nltk.tokenize.treebank import TreebankWordTokenizer
import numpy as np
from sklearn.neighbors import NearestNeighbors

from .forms import (CreateUserDrinkForm, CreateUserDrinkIngredientForm, CreateUserDrinkInstructionForm,
                    ProfileUpdateForm, UserRegisterForm, UserUpdateForm)
from .models import (Comment, Drink, Friend, FriendRequest, Profile, ProfileToDislikedDrink, ProfileToLikedDrink,
                     UserDrink)

up_ratio, down_ratio = 0.1, 0.05


def bad_request(request):
    """
    Bad Request View
    """

    return HttpResponseRedirect(reverse('home'))


def home(request):
    """
    Home View
    """
    if request.user.is_authenticated:

        profile = Profile.objects.get(user=request.user)
        if ProfileToLikedDrink.objects.filter(profile=profile) or ProfileToLikedDrink.objects.filter(profile=profile):

            print(f'USERNAME: {profile.user}')
            # Load ratings (we account for exact column indices changing based on enumerate() returns)
            drinks = Drink.objects.all()
            hash2column = {}
            column2hash = {}
            for i, drink in enumerate(drinks):
                hash2column[drink.drink_hash] = i
                column2hash[i] = drink.drink_hash
            ratings = np.zeros((840, len(drinks))) # (|profiles|, |drinks|) when ratings were recorded
            with open('static/data/ratings.db') as f:
                for line in f.readlines():
                    terms = line.split(',')
                    ratings[int(terms[0]), hash2column[terms[1]]] = int(terms[2])

            # Create user's profile rating vector
            profile_ratings = np.zeros(len(drinks))
            for like in ProfileToLikedDrink.objects.filter(profile=profile):
                profile_ratings[hash2column[like.drink.drink_hash]] = 1
            for dislike in ProfileToDislikedDrink.objects.filter(profile=profile):
                profile_ratings[hash2column[dislike.drink.drink_hash]] = -1

            # Normalize ratings by subtracting each profile's average rating
            profile_masked = np.ma.masked_array(profile_ratings, mask=(profile_ratings == 0), fill_value=0)
            profile_average = np.average(profile_masked)
            profile_ratings = np.array(profile_masked - profile_average)

            masked = np.ma.masked_array(ratings, mask=(ratings == 0), fill_value=0)
            average = np.average(masked, axis=1)
            ratings = np.array(masked - average.reshape((average.shape[0], 1)))

            k = 3
            nn = NearestNeighbors(n_neighbors=k).fit(ratings)
            indices = nn.kneighbors(profile_ratings.reshape(1, len(profile_ratings)), return_distance=False)[0]
            neighbors = ratings[indices]
            scores = np.sum(neighbors, axis=0) / k
            indices = np.argsort(scores)
            hashes = []
            for i in indices[::-1]:
                if profile_ratings[i] == 0: # only use this rec if the user hasn't already rated this drink
                    hashes.append(column2hash[i])
                if len(hashes) == k:
                    break

            response = [0 for i in range(k)]
            discovery_adapter = drink_adapter.DiscoveryAdapter()
            futures = {}
            with concurrent.futures.ThreadPoolExecutor(max_workers=k) as executor:
                for i, d_hash in enumerate(hashes):
                    futures[executor.submit(discovery_adapter.get_drink, d_hash)] = d_hash
                idx = 0
                for future in concurrent.futures.as_completed(futures):
                    response[idx] = future.result()[0]
                    idx += 1
            
            '''
            # Update ratings.db (takes about ~120s with the fake db)
            drinks = Drink.objects.all()
            profiles = Profile.objects.all()
            rows = {}
            for i, profile in enumerate(profiles):
                rows[profile] = i
            with open('static/data/ratings.db', 'w') as f:
                # Populate ratings matrix
                for like in ProfileToLikedDrink.objects.all():
                    row = rows[like.profile]
                    rating = 1
                    f.write('%d,%s,%d\n' % (row, like.drink.drink_hash, rating))
                for dislike in ProfileToDislikedDrink.objects.all():
                    row = rows[dislike.profile]
                    rating = -1
                    f.write('%d,%s,%d\n' % (row, dislike.drink.drink_hash, rating))
            '''
        else:
            response = {}
    else:
        response = {}

    return render(request, 'gnt/index.html', {'drinks':response})


def _text_to_dql(text, name_multiplier=1, ingredient_multiplier=1):
    """Converts user input text queries to DQL queries."""
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
    # additional stopwords that help specific searches
    stopwords += ['drinks', 'recommend']
    # negation stopwords not from any source, we may need to add to this list as we test
    negation_stopwords = ["n't", 'no', 'not',
                          'nor', 'none', 'never', 'without']
    # split user input into manageable tokens
    tokens = TreebankWordTokenizer().tokenize(
        text)  # NLTKWordTokenizer supposed to be "improved", but destructive module not found
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
            positive += 'names:"%s"^%d' % (token, name_multiplier)
            positive += '|'
            positive += 'ingredients:"%s"^%d' % (token, ingredient_multiplier)
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
    return query


def _query_discovery(text, question, offset=0):
    """Creates a DQL query based on text and question, then queries discovery.

    :param text:
    :param question:
    :param offset:
    :return:
    """
    # Perform slightly different searches based on what kind of question the user is asking
    if question == 'how':
        query = _text_to_dql(text, 2, 1)  # make drink names more important
    else:
        # make drink ingredients more important
        query = _text_to_dql(text, 1, 2)

    discovery_adapter = drink_adapter.DiscoveryAdapter()
    response = discovery_adapter.search(query, offset=offset)

    if question == 'like':
        # if user is looking for similar drinks to a given drink, remove the given drink from the response
        for i, drink in enumerate(response):
            if drink['names'][0].lower() in text.lower():
                response.pop(i)
                break

    return response



def results(request):
    """
    Results View
    """
    if request.method == 'POST':
        if 'audio' in request.FILES:
            audio = request.FILES['audio']
            text = IBM().transcribe(audio)
            if 'recommend' in text:
                question = 'like'
            else:
                question = 'what'
        else:
            text = request.POST['search_bar']
            question = request.POST['question']

        response = _query_discovery(text, question)

        return render(request, 'gnt/results.html', {
            'query': text,
            'drinks': response,
            'question': question
        })
    else:
        return HttpResponseRedirect(reverse('home'))


def more_results(request):
    """
    More results with an offset
    """
    response = _query_discovery(
        request.POST['text'], request.POST['question'], request.POST['offset'])

    return render(request, 'gnt/drink_results_with_voting.html', {
        'query': request.POST['text'],
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

    ingredient_formset = formset_factory(CreateUserDrinkIngredientForm)
    instruction_formset = formset_factory(CreateUserDrinkInstructionForm)

    if request.method == 'POST':
        create_user_drink_form = CreateUserDrinkForm(
            request.POST, request.FILES)

        if create_user_drink_form.is_valid():
            drink = create_user_drink_form.save(commit=False)
            drink.user = request.user
            drink.save()

            ingredient_formset = ingredient_formset(
                request.POST, prefix='ingredient')
            if ingredient_formset.is_valid():
                for ingredient_form in ingredient_formset:
                    ingredient = ingredient_form.save(commit=False)
                    ingredient.drink = drink
                    ingredient.save()

            instruction_formset = instruction_formset(
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
            return redirect('timeline', username=request.user.username)
    else:
        create_user_drink_form = CreateUserDrinkForm()
        ingredient_formset = ingredient_formset(prefix='ingredient')
        instruction_formset = instruction_formset(prefix='instruction')

    context = {
        'profile': username,
        'create_user_drink_form': create_user_drink_form,
        'ingredient_formset': ingredient_formset,
        'instruction_formset': instruction_formset
    }

    return render(request, 'gnt/profile_create_drink.html', context)


def profile_public(request, username):
    """
    Profile View

    Users, unauthenticated and authenticated, can view other users' profiles with
    this view function. The profile view will render a list of drinks created by
    the user of the profile.

    Args:
        request: request object provided by django
        username (string): the user of the profile

    Return:
        profile_public (html): profile view of given username
    """

    # get user
    user = User.objects.get(username=username)

    # get drinks created by user ordered by new
    drinks = UserDrink.objects.filter(user=user).order_by('-timestamp')

    # if post request
    if request.method == 'POST':

        # if add friend post request
        if 'add-friend' in request.POST:
            friend_request = FriendRequest()
            friend_request.requestee = user.profile
            friend_request.requestor = request.user.profile
            friend_request.save()

            messages.success(request, f'Friend request sent to { username }!')

        # else if remove friend post request
        elif 'remove-friend' in request.POST:
            friend = Friend.objects.filter(friend1=request.user.profile, friend2=user.profile) | Friend.objects.filter(
                friend1=user.profile, friend2=request.user.profile)
            friend.delete()

            messages.success(request, f'Removed friend { username }!')

        # else if create comment post request
        elif 'create-comment' in request.POST:
            drink = UserDrink.objects.get(id=request.POST['drink'])

            comment = Comment(
                author=request.user,
                drink=drink,
                comment=request.POST['create-comment']
            )

            comment.save()

            messages.success(
                request, f'You left a comment on { username }\'s drink!')

        elif 'accept-friend' in request.POST:
            friend_request = FriendRequest.objects.get(requestee=request.user.profile, requestor=user.profile)
            friend_request.delete()

            friend = Friend(
                friend1=request.user.profile,
                friend2=user.profile
            )

            friend.save()

            messages.success(request, f'You have accepted { username }\'s friend request!')

        elif 'deny-friend' in request.POST:
            friend_request = FriendRequest.objects.get(requestee=request.user.profile, requestor=user.profile)
            friend_request.delete()

            messages.info(request, f'You have denied to add { username } as a friend.')

    requests = []
    friends = []
    if request.user.is_authenticated:
        requests = FriendRequest.objects.filter(Q(requestee=request.user.profile, requestor=user.profile) |
                                                Q(requestee=user.profile, requestor=request.user.profile))
        friends = Friend.objects.filter(Q(friend1=request.user.profile, friend2=user.profile) |
                                        Q(friend1=user.profile, friend2=request.user.profile))

        if requests:
            requests = requests[0]

        if friends:
            friends = friends[0]

    context = {
        'profile': user,
        'drinks': drinks,
        'requests': requests,
        'friends': friends,
    }

    return render(request, 'gnt/profile_public.html', context)


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
            return redirect('timeline', username=request.user.username)
    else:
        user_update_form = UserUpdateForm(instance=username)
        profile_update_form = ProfileUpdateForm(instance=profile)

    context = {
        'profile': username,
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'gnt/profile_edit.html', context)


def liked_drinks(request, username):
    """
    Liked Drinks View
    """

    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)

    # if post request
    if request.method == 'POST':

        # if add friend post request
        if 'add-friend' in request.POST:
            friend_request = FriendRequest()
            friend_request.requestee = user.profile
            friend_request.requestor = request.user.profile
            friend_request.save()

            messages.success(request, f'Friend request sent to { username }!')

        # else if remove friend post request
        elif 'remove-friend' in request.POST:
            friend = Friend.objects.filter(friend1=request.user.profile, friend2=user.profile) | Friend.objects.filter(
                friend1=user.profile, friend2=request.user.profile)
            friend.delete()

            messages.success(request, f'Removed friend { username }!')

        elif 'accept-friend' in request.POST:
            friend_request = FriendRequest.objects.get(requestee=request.user.profile, requestor=user.profile)
            friend_request.delete()

            friend = Friend(
                friend1=request.user.profile,
                friend2=user.profile
            )

            friend.save()

            messages.success(request, f'You have accepted { username }\'s friend request!')

        elif 'deny-friend' in request.POST:
            friend_request = FriendRequest.objects.get(requestee=request.user.profile, requestor=user.profile)
            friend_request.delete()

            messages.info(request, f'You have denied to add { username } as a friend.')

    requests = []
    friends = []
    if request.user.is_authenticated:
        requests = FriendRequest.objects.filter(Q(requestee=request.user.profile, requestor=user.profile) |
                                                Q(requestee=user.profile, requestor=request.user.profile))
        friends = Friend.objects.filter(Q(friend1=request.user.profile, friend2=user.profile) |
                                        Q(friend1=user.profile, friend2=request.user.profile))

        if requests:
            requests = requests[0]

        if friends:
            friends = friends[0]

    profile_to_drink = ProfileToLikedDrink.objects.filter(profile=profile.id)

    if profile_to_drink:
        response = [0 for i in range(len(profile_to_drink))]

        discovery_adapter = drink_adapter.DiscoveryAdapter()
        futures = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(profile_to_drink)) as executor:
            for i, ptd in enumerate(profile_to_drink):
                drink = Drink.objects.get(id=ptd.drink.id)
                futures[executor.submit(discovery_adapter.get_drink, drink.drink_hash)] = drink.drink_hash
            idx = 0
            for future in concurrent.futures.as_completed(futures):
                response[idx] = future.result()[0]
                idx += 1

        context = {
            'profile': user,
            'drinks': response,
            'requests': requests,
            'friends': friends
        }

        return render(request, 'gnt/profile_liked_drinks.html', context)

    else:
        context = {
            'profile': user,
            'requests': requests,
            'friends': friends
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

    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)

    # if post request
    if request.method == 'POST':

        # if add friend post request
        if 'add-friend' in request.POST:
            friend_request = FriendRequest()
            friend_request.requestee = user.profile
            friend_request.requestor = request.user.profile
            friend_request.save()

            messages.success(request, f'Friend request sent to { username }!')

        # else if remove friend post request
        elif 'remove-friend' in request.POST:
            friend = Friend.objects.filter(friend1=request.user.profile, friend2=user.profile) | Friend.objects.filter(
                friend1=user.profile, friend2=request.user.profile)
            friend.delete()

            messages.success(request, f'Removed friend { username }!')

        elif 'accept-friend' in request.POST:
            friend_request = FriendRequest.objects.get(requestee=request.user.profile, requestor=user.profile)
            friend_request.delete()

            friend = Friend(
                friend1=request.user.profile,
                friend2=user.profile
            )

            friend.save()

            messages.success(request, f'You have accepted { username }\'s friend request!')

        elif 'deny-friend' in request.POST:
            friend_request = FriendRequest.objects.get(requestee=request.user.profile, requestor=user.profile)
            friend_request.delete()

            messages.info(request, f'You have denied to add { username } as a friend.')

    requests = []
    friends = []
    if request.user.is_authenticated:
        requests = FriendRequest.objects.filter(Q(requestee=request.user.profile, requestor=user.profile) |
                                                Q(requestee=user.profile, requestor=request.user.profile))
        friends = Friend.objects.filter(Q(friend1=request.user.profile, friend2=user.profile) |
                                        Q(friend1=user.profile, friend2=request.user.profile))

        if requests:
            requests = requests[0]

        if friends:
            friends = friends[0]

    profile_to_drink = ProfileToDislikedDrink.objects.filter(profile=profile.id)

    if profile_to_drink:
        response = [0 for i in range(len(profile_to_drink))]

        discovery_adapter = drink_adapter.DiscoveryAdapter()
        futures = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(profile_to_drink)) as executor:
            for i, ptd in enumerate(profile_to_drink):
                drink = Drink.objects.get(id=ptd.drink.id)
                futures[executor.submit(discovery_adapter.get_drink, drink.drink_hash)] = drink.drink_hash
            idx = 0
            for future in concurrent.futures.as_completed(futures):
                response[idx] = future.result()[0]
                idx += 1

        context = {
            'profile': user,
            'drinks': response,
            'requests': requests,
            'friends': friends
        }

        return render(request, 'gnt/profile_disliked_drinks.html', context)

    else:

        context = {
            'profile': user,
            'requests': requests,
            'friends': friends
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
    up_thresh = len(Profile.objects.all()) * up_ratio
    down_thresh = 0 - len(Profile.objects.all()) * down_ratio
    context = {
        'drinks': drinks,
        'up_thresh': up_thresh,
        'down_thresh': down_thresh
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
    up_thresh = len(Profile.objects.all()) * up_ratio
    down_thresh = 0 - len(Profile.objects.all()) * down_ratio
    context = {
        'drinks': drinks,
        'up_thresh': up_thresh,
        'down_thresh': down_thresh
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
            friend_request = FriendRequest.objects.get(requestee=request.user.profile, requestor=requestor.profile)
            friend_request.delete()
            friend = Friend(friend1=request.user.profile, friend2=requestor.profile)
            friend.save()

            messages.success(request, f'You have added friend { requestor.profile.user }!')

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

    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)

    # if post request
    if request.method == 'POST':

        # if add friend post request
        if 'add-friend' in request.POST:
            friend_request = FriendRequest()
            friend_request.requestee = user.profile
            friend_request.requestor = request.user.profile
            friend_request.save()

            messages.success(request, f'Friend request sent to { username }!')

        # else if remove friend post request
        elif 'remove-friend' in request.POST:
            friend = Friend.objects.filter(friend1=request.user.profile, friend2=user.profile) | \
                     Friend.objects.filter(friend1=user.profile, friend2=request.user.profile)
            friend.delete()

            messages.success(request, f'Removed friend { username }!')

        elif 'accept-friend' in request.POST:
            friend_request = FriendRequest.objects.get(requestee=request.user.profile, requestor=user.profile)
            friend_request.delete()

            friend = Friend(
                friend1=request.user.profile,
                friend2=user.profile
            )

            friend.save()

            messages.success(request, f'You have accepted { username }\'s friend request!')

        elif 'deny-friend' in request.POST:
            friend_request = FriendRequest.objects.get(requestee=request.user.profile, requestor=user.profile)
            friend_request.delete()

            messages.info(request, f'You have denied to add { username } as a friend.')

    requests = []
    if request.user.is_authenticated:
        requests = FriendRequest.objects.filter(Q(requestee=request.user.profile, requestor=user.profile) |
                                                Q(requestee=user.profile, requestor=request.user.profile))

        if requests:
            requests = requests[0]

    friends = Friend.objects.filter(friend1=profile) | Friend.objects.filter(
        friend2=profile)

    context = {
        'profile': user,
        'requests': requests,
        'friends': friends
    }

    return render(request, 'gnt/profile_friends.html', context)
