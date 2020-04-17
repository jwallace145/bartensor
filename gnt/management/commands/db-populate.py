import json
import os
from random import randint
from random import random

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand

from gnt.models import (Drink, DrinkName, Ingredient, Instruction, Profile,
                        UserDrink, ProfileToLikedDrink, ProfileToDislikedDrink)
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV1


class Command(BaseCommand):

    def _create_tags(self):
        environment_id = 'b7d1486c-2fdc-40c5-a2ce-2d78ec48fa76'
        collection_id = '7c11f329-5f31-4e59-aa63-fde1e91ff681'
        authenticator = IAMAuthenticator(
            getattr(settings, 'WATSON_DISCOVERY_API_KEY', None))
        discovery = DiscoveryV1(version='2019-04-30',
                                authenticator=authenticator)
        discovery.set_service_url(
            'https://api.us-south.discovery.watson.cloud.ibm.com/')
        response = discovery.query(environment_id, collection_id, _return=[
                                   'id', 'names'], count='1000').result['results']
        for i in response:
            id_var = i['id']
            print(f'INSERTING {id_var}', file=self.stdout)
            d = Drink(drink_hash=id_var)
            d.save()
            names_arr = i['names']
            d = Drink.objects.get(drink_hash=id_var)
            for name in names_arr:
                print(f'INSERTING {str(name)}', file=self.stdout)
                d_name = DrinkName(drink=d, drink_name=name)
                d_name.save()

    def _create_fake_users(self):
        user = User.objects.create_superuser(
            username="Caleb",
            email="caleb@gmail.com",
            password='password'
        )
        profile = Profile.objects.get(user=user)
        profile.bio = 'B2B Flip Cup Champ'
        profile.image = 'profile_pics/6d4.jpg'
        profile.save()
        print('CREATED ADMIN ACCOUNT USERNAME: Caleb, PASSWORD: password')

        user = User.objects.create_superuser(
            username="Jimmy",
            email="jimmy@gmail.com",
            password='password'
        )
        profile = Profile.objects.get(user=user)
        profile.bio = 'Keep it 300'
        profile.image = 'profile_pics/chance.jpeg'
        profile.save()
        print('CREATED ADMIN ACCOUNT USERNAME: Jimmy, PASSWORD: password')

        user = User.objects.create_superuser(
            username="Eric",
            email="Eric@gmail.com",
            password='password'
        )
        profile = Profile.objects.get(user=user)
        profile.bio = 'Hide yo girl bruh'
        profile.image = 'profile_pics/dababy.jpeg'
        profile.save()
        print('CREATED ADMIN ACCOUNT USERNAME: Eric, PASSWORD: password')

        user = User.objects.create_superuser(
            username="Michael",
            email="Michael@gmail.com",
            password='password'
        )
        profile = Profile.objects.get(user=user)
        profile.bio = 'They call me Dirty Mike'
        profile.image = 'profile_pics/kanye.jpeg'
        profile.save()
        print('CREATED ADMIN ACCOUNT USERNAME: Michael, PASSWORD: password')

        user = User.objects.create_superuser(
            username="Jack",
            email="Jack@gmail.com",
            password='password'
        )
        profile = Profile.objects.get(user=user)
        profile.bio = 'I once ate a whole jar of peanut butter without using my hands'
        profile.image = 'profile_pics/jcole.jpg'
        profile.save()
        print(f'CREATED ADMIN ACCOUNT USERNAME: Jack, PASSWORD: password')

    def _create_fake_likes(self):
        max_fake_users = int(1.5 * len(Drink.objects.all()))
        for i in range(max_fake_users):
            User.objects.create_user(username=f'User{i}', email=f'user{i}@gmail.com', password='password')
            u = User.objects.get(username=f'User{i}')
            print(f'CREATED ACCOUNT USERNAME: User{i}/{max_fake_users}')
            actions = randint(0, int(len(Drink.objects.all()) / 4))
            for j in range(actions):
                k = randint(1, len(Drink.objects.all()))
                d = Drink.objects.get(id=k)
                if random() >= 0.25:
                    print(f'    User{i} liked drink {k}/{actions}')
                    ld = ProfileToLikedDrink(profile=u.profile, drink=d)
                    ld.save()
                else:
                    print(f'    User{i} disliked drink {k}/{actions}')
                    dd = ProfileToDislikedDrink(profile=u.profile, drink=d)
                    dd.save()
        
    def handle(self, *args, **options):
        print('DELETING DB')
        os.system("del /f db.sqlite3")
        os.system('python manage.py makemigrations')
        os.system('python manage.py migrate')
        self._create_tags()
        self._create_fake_users()
        self._create_fake_likes()
        print('TRANSACTION COMPLETE', file=self.stdout)
