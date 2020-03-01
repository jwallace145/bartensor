from django.core.management.base import BaseCommand, CommandError
from gnt.models import Drinks, Drink_names
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from django.conf import settings

class Command(BaseCommand):

    def _create_tags(self):
        environment_id = 'b7d1486c-2fdc-40c5-a2ce-2d78ec48fa76'
        collection_id = '7c11f329-5f31-4e59-aa63-fde1e91ff681'

        authenticator = IAMAuthenticator(getattr(settings, 'WATSON_DISCOVERY_API_KEY', None))
        discovery = DiscoveryV1(version='2019-04-30',authenticator=authenticator)
        discovery.set_service_url('https://api.us-south.discovery.watson.cloud.ibm.com/')
        response = discovery.query(environment_id, collection_id, _return=['id','names'], count='1000').result['results']
        for i in response:
            id_var = i['id']
            print(f'INSERTING {id_var}', file=self.stdout)
            d = Drinks(drink_hash=id_var)
            d.save()
            names_arr = i['names']
            d = Drinks.objects.get(drink_hash=id_var)
            for name in names_arr:
                print(f'INSERTING {str(name)}', file=self.stdout)
                d_name = Drink_names(drink_FK = d, drink_name=name)
                d_name.save()

    def handle(self, *args, **options):
        self._create_tags()
        print('TRANSACTION COMPLETE', file=self.stdout)
        