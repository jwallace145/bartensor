from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator 

# Target Interface
class DrinkInterface():
    """
    Drink results used by client. Form of {id: '...', names: ['...', '...'], ingredients: ['...', '...'],
    method: ['...', '...']}
    """
    def drink_search(self, text):
        raise NotImplementedError()


# Adaptee
class DiscoveryDrinks():
    """
    Response from Discovery which is incompatible with client code
    """

    def natural_language_query(self, text):
        raise NotImplementedError()

    def liked_drinks(self, user):
        raise NotImplementedError()

    def disliked_drinks(self, user):
        raise NotImplementedError()

    def discovery_query_language(self, queryparams):
        raise NotImplementedError()

# Adapter
class DiscoveryAdapter(DrinkInterface):
    """
    The Discovery Adapter makes Discovery's response interface compatible with the Drink Results interface
    """

