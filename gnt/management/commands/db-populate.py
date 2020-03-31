from django.core.management.base import BaseCommand
from gnt.models import Drink, DrinkName, UserDrink, Profile
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from django.conf import settings
from django.contrib.auth.models import User
import os
from django.core.files import File


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
        profile.image = 'profile_pics/6d4.jpeg'
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

        drink_images_folder = [
            x[0] + '/' for x in os.walk('gnt/static/data/drink_images/')]
        drink_images_folder = drink_images_folder[2:]
        for i in range(100):
            User.objects.create_user(
                username=f'User{i}', email=f'user{i}@gmail.com', password='password')
            u = User.objects.get(username=f'User{i}')
            print(
                f'CREATED ACCOUNT USERNAME: User{i}, PASSWORD: password', end='\t')
            for img in os.listdir(drink_images_folder[i]):
                path = drink_images_folder[i] + img
            im = open(path, 'rb')
            django_file = File(im)
            user_d = UserDrink(
                user=u, name=f'drink{i}', description=f'description{i}', image=django_file)
            user_d.save()
            print(f'CREATED USER DRINK: drink{i}')

    def handle(self, *args, **options):
        self._create_fake_users()
        self._create_tags()
        print('TRANSACTION COMPLETE', file=self.stdout)
