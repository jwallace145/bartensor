from django.http import JsonResponse
from gnt.models import Profile, Drink, DrinkName, ProfileToLikedDrink, ProfileToDislikedDrink


def like_drink(request):
    try:
        username = request.POST['user']
        drink = Drink.objects.get(drink_hash=request.POST['drink_id'])

        profile = Profile.objects.get(id=request.user.profile.id)

        # Check to see if drink is disliked then remove
        disliked_drink = ProfileToDislikedDrink.objects.filter(
            profile=profile, drink=drink)
        if disliked_drink:
            disliked_drink.delete()

        if ProfileToLikedDrink.objects.filter(profile=profile, drink=drink):
            response = {
                'message': "Drink " + str(request.POST['drink_id']) + " has already been liked by " + str(username) + ". No changes to db",
                'status': 422
            }
        else:
            new_like = ProfileToLikedDrink(profile=profile, drink=drink)
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
        drink = Drink.objects.get(drink_hash=request.POST['drink_id'])
        profile = Profile.objects.get(id=request.user.profile.id)

        # If user has liked drink, remove it from liked table
        liked_drink = ProfileToLikedDrink.objects.filter(
            profile=profile, drink=drink)

        if liked_drink:
            # Remove liked drink
            liked_drink.delete()

        if ProfileToDislikedDrink.objects.filter(profile=profile, drink=drink):
            response = {
                'message': "Drink " + str(request.POST['drink_id']) + " has already been disliked by " + str(username) + ". No changes to db",
                'status': 422
            }
        else:
            new_dislike = ProfileToDislikedDrink(profile=profile, drink=drink)
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
        drink = Drink.objects.get(drink_hash=request.POST['drink_id'])
        profile = Profile.objects.get(id=request.user.profile.id)
        liked_drink = ProfileToLikedDrink.objects.filter(
            profile=profile, drink=drink)
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


def remove_disliked_drink(request):
    try:
        username = request.POST['user']
        drink = Drink.objects.get(drink_hash=request.POST['drink_id'])
        profile = Profile.objects.get(id=request.user.profile.id)
        disliked_drink = ProfileToDislikedDrink.objects.filter(
            profile=profile, drink=drink)

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


def get_liked_disliked_drinks(request):
    try:
        liked_drinks = []
        disliked_drinks = []
        user = request.user
        profile = Profile.objects.get(user=user)
        # get liked drinks
        profile_to_liked_drink = ProfileToLikedDrink.objects.filter(
            profile=profile)
        if profile_to_liked_drink:
            response = [0 for i in range(len(profile_to_liked_drink))]
            for i, ptd in enumerate(profile_to_liked_drink):
                response[i] = ptd.drink.drink_hash
            liked_drinks = response
        # get disliked drinks
        profile_to_disliked_drink = ProfileToDislikedDrink.objects.filter(
            profile=profile)
        if profile_to_disliked_drink:
            response = [0 for i in range(len(profile_to_disliked_drink))]
            for i, ptd in enumerate(profile_to_disliked_drink):
                response[i] = ptd.drink.drink_hash
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
