from django.http import JsonResponse
from .models import Profile, Drinks, Drink_names, Profile_to_liked_drink, Profile_to_disliked_drink

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

def get_liked_disliked_drinks(request):
    try:
        print('here')
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
        print('error')
        print(str(e))
        response = {
            'message': str(e),
            'status': 500
        }
        return JsonResponse(response)