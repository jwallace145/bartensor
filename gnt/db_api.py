from django.http import JsonResponse
from gnt.models import Profile, Drink, DrinkName, ProfileToLikedDrink, ProfileToDislikedDrink, UpvotedUserDrink, DownvotedUserDrink, UserDrink, Ingredient, Instruction
import json
import os
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from django.conf import settings
from django.contrib import messages
import threading
import shutil
import time

up_ratio, down_ratio = 0.1, 0.05

api_key = getattr(settings, 'WATSON_DISCOVERY_API_KEY', None)
environment_id = 'b7d1486c-2fdc-40c5-a2ce-2d78ec48fa76'
collection_id = '7c11f329-5f31-4e59-aa63-fde1e91ff681'
authenticator = IAMAuthenticator(api_key)
discovery = DiscoveryV1(version='2019-04-30', authenticator=authenticator)
discovery.set_service_url(
    'https://api.us-south.discovery.watson.cloud.ibm.com/')

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

def get_liked_disliked_user_drinks(request):
    try:
        liked_drinks = []
        disliked_drinks = []
        user = request.user
        profile = Profile.objects.get(user=user)
        # get liked drinks
        profile_to_liked_drink = UpvotedUserDrink.objects.filter(
            profile=profile)
        if profile_to_liked_drink:
            response = [0 for i in range(len(profile_to_liked_drink))]
            for i, ptd in enumerate(profile_to_liked_drink):
                response[i] = ptd.drink.id
            liked_drinks = response
        # get disliked drinks
        profile_to_disliked_drink = DownvotedUserDrink.objects.filter(
            profile=profile)
        if profile_to_disliked_drink:
            response = [0 for i in range(len(profile_to_disliked_drink))]
            for i, ptd in enumerate(profile_to_disliked_drink):
                response[i] = ptd.drink.id
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

def like_user_drink(request):
    try:
        username = request.POST['user']
        drink = UserDrink.objects.get(id=request.POST['drink_id'])
        profile = Profile.objects.get(id=request.user.profile.id)
        if DownvotedUserDrink.objects.filter(profile=profile, drink=drink):
            disliked_drink = DownvotedUserDrink.objects.filter(profile=profile, drink=drink)
            disliked_drink.delete()
            drink.votes += 2
            drink.save()
            new_like = UpvotedUserDrink(profile=profile, drink=drink)
            new_like.save()
            message = "Drink " + \
                str(request.POST['drink_id']) + "added to " + \
                str(username) + "'s liked drinks"
            status = 201
        elif UpvotedUserDrink.objects.filter(profile=profile, drink=drink):
            upvoted_drink = UpvotedUserDrink.objects.filter(profile=profile, drink=drink)
            upvoted_drink.delete()
            drink.votes -= 1
            drink.save()
            message =  "Removed the upvote"
            status =  202
        else:
            new_like = UpvotedUserDrink(profile=profile, drink=drink)
            new_like.save()
            drink.votes += 1
            drink.save()
            message = "Drink " + \
                str(request.POST['drink_id']) + "added to " + \
                str(username) + "'s liked drinks"
            status = 201
        up_thresh = len(Profile.objects.all()) * up_ratio
        if drink.votes > up_thresh:
            print(f'UP THRESHOLD: {up_thresh}')
            print(f'{drink.name} HAS BEEN ADDED TO DISCOVERY')
            drink_image_url = drink.image.url
            drink_id = drink.id
            drink_copied_filepath = make_drink_json(drink)
            drink.delete()
            x = threading.Thread(target=upload_to_discovery, args=(drink_id, drink_copied_filepath, ))
            x.start()
            message =  "Drink has been added to discovery"
        response = {
            'message': message,
            'status': status
        }
        return JsonResponse(response)
    except Exception as e:
        print(str(e))
        response = {
            'message': str(e),
            'status': 500
        }
        return JsonResponse(response)

def make_drink_json(drink):
    names = [drink.name]
    ingredients = [f'{ingr.quantity} {ingr.name}' for ingr in Ingredient.objects.filter(drink=drink)]
    instructions = [f'{instr.instruction}' for instr in Instruction.objects.filter(drink=drink)]
    json_obj = {"names": names,
                "ingredients": ingredients,
                "method": instructions,
                "picture": "userdrink.jpg"}
    print(json.dumps(json_obj))
    path = f'gnt/static/data/accepted_user_drinks/User_drink{drink.id}/User_drink{drink.id}.json'
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(path, 'w') as outfile:
        json.dump(json_obj, outfile)
    outfile.close()
    print(drink.image.url[1:])
    shutil.copy(drink.image.url[1:], f'gnt/static/data/accepted_user_drinks/User_drink{drink.id}')
    img_name = os.path.basename(drink.image.url[1:])
    return f'gnt/static/data/accepted_user_drinks/User_drink{drink.id}/{img_name}'


def upload_to_discovery(drink_id, image_url):
    print("Hyperthread engaged")
    with open(f'./gnt/static/data/accepted_user_drinks/User_drink{drink_id}/User_drink{drink_id}.json') as fileinfo:
        add_doc = discovery.add_document(f'{environment_id}', f'{collection_id}', file=fileinfo).get_result()
    fileinfo.close()
    d_id, d_status = add_doc['document_id'], add_doc['status']
    print(f'DOCUMENT {d_id} IS {d_status}')
    dest_path = f'gnt/static/data/drink_images/{d_id}/img_{d_id}.jpg'
    dirname = os.path.dirname(dest_path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    shutil.move(image_url, dest_path)
    response = []
    while len(response) == 0:
        response = discovery.query(environment_id, collection_id, query=f'id::"{d_id}"').result['results']
        if len(response) == 0:
            time.sleep(10)
        print(f'RESPONSE: {response}')
    for i in response:
        id_var = i['id']
        print(f'INSERTING {id_var}')
        d = Drink(drink_hash=id_var)
        d.save()
        print(f'{id_var} INSERTED', end='\t')
        names_arr = i['names']
        d = Drink.objects.get(drink_hash=id_var)
        for name in names_arr:
            print(f'INSERTING {str(name)}')
            d_name = DrinkName(drink=d, drink_name=name)
            print(f'{name} INSERTED')
            d_name.save()


def dislike_user_drink(request):
    try:
        username = request.POST['user']
        drink = UserDrink.objects.get(id=request.POST['drink_id'])
        profile = Profile.objects.get(id=request.user.profile.id)
        if UpvotedUserDrink.objects.filter(profile=profile, drink=drink):
            liked_drink = UpvotedUserDrink.objects.filter(profile=profile, drink=drink)
            liked_drink.delete()
            drink.votes -= 2
            drink.save()
            new_dislike = DownvotedUserDrink(profile=profile, drink=drink)
            new_dislike.save()
            message = "Drink " + \
                str(request.POST['drink_id']) + "added to " + \
                str(username) + "'s disliked drinks"
            status = 201
        elif DownvotedUserDrink.objects.filter(profile=profile, drink=drink):
            downvoted_drink = DownvotedUserDrink.objects.filter(profile=profile, drink=drink)
            downvoted_drink.delete()
            drink.votes += 1
            drink.save()
            message = "Removed the downvote"
            status = 202
        else:
            new_dislike = DownvotedUserDrink(profile=profile, drink=drink)
            new_dislike.save()
            drink.votes -= 1
            drink.save()
            message = "Drink " + \
                str(request.POST['drink_id']) + "added to " + \
                str(username) + "'s disliked drinks"
            status = 201
        down_thresh = 0 - (len(Profile.objects.all()) * down_ratio)
        if drink.votes < down_thresh:
            print(f'DOWN THRESHOLD: {down_thresh}')
            drink.delete()
            print(f'{drink.name} SUCKS TOO MUCH AND HAS BEEN DELETED')
            message = f'{drink.name} has reach the downvote threshold of {down_thresh} and has been deleted!'
            
        response = {
            'message': message,
            'status': status
        }
        return JsonResponse(response)
    except Exception as e:
        print(str(e))
        response = {
            'message': str(e),
            'status': 500
        }
        return JsonResponse(response)


