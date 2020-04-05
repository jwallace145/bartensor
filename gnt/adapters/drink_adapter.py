from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from django.conf import settings

api_key = getattr(settings, 'WATSON_DISCOVERY_API_KEY', None)
environment_id = 'b7d1486c-2fdc-40c5-a2ce-2d78ec48fa76'
collection_id = '7c11f329-5f31-4e59-aa63-fde1e91ff681'
authenticator = IAMAuthenticator(api_key)
discovery = DiscoveryV1(version='2019-04-30', authenticator=authenticator)
discovery.set_service_url(
    'https://api.us-south.discovery.watson.cloud.ibm.com/')


# Target Interface
class DrinkInterface():
    """
    Drink results used by client. Form of {id: '...', names: ['...', '...'], ingredients: ['...', '...'],
    method: ['...', '...']}
    """

    def natural_language_search(self, text):
        raise NotImplementedError()

    def natural_language_search_offset(self, text, offset):
        raise NotImplementedError()

    def search(self, query):
        raise NotImplementedError()

    def get_drink(self, drink_id):
        raise NotImplementedError()


class DiscoveryAdaptee():
    """
    Response from Discovery which is incompatible with client code
    """

    def natural_language_search(self, text):
        return discovery.query(
            environment_id, collection_id, natural_language_query=text).result['results']

    def natural_language_search_offset(self, text, offset):
        return discovery.query(
            environment_id, collection_id, natural_language_query=text, offset=offset).result['results']

    def search(self, query):
        return discovery.query(environment_id, collection_id, query=text).result['results']

    def get_drink(self, drink_id):
        return discovery.query(
            environment_id, collection_id, query=f'id::"{drink_id}"').result['results']

class DiscoveryAdapter(DrinkInterface):
    """
    The Discovery Adapter makes Discovery's response interface compatible with the Drink Results interface
    """

    def __init__(self):
        self.adaptee = DiscoveryAdaptee()

    def natural_language_search(self, text):
        return self.adaptee.natural_language_search(text)

    def natural_language_search_offset(self, text, offset):
        return self.adaptee.natural_language_search_offset(text, offset)

    def search(self, query):
        return self.adaptee.search(query)

    def get_drink(self, drink_id):
        return self.adaptee.get_drink(drink_id)
