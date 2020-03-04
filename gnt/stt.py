'''
Speech-to-text adapter and implementing classes.
'''
from django.conf import settings

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class STT:
    def __init__(self):
        raise NotImplementedError('Speech-to-text adapter not implemented')

    def transcribe(self, audio):
        raise NotImplementedError('transcribe() not implemented in speech-to-text adapter')

class IBM(STT):
    def __init__(self):
        api_key = getattr(settings, 'WATSON_SPEECH_TO_TEXT_API_KEY', None)

        authenticator = IAMAuthenticator(api_key)
        self.speech_to_text = SpeechToTextV1(authenticator=authenticator)

        self.speech_to_text.set_service_url('https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/678b9838-b572-44d3-a3c1-66cf47ce9d67')

    def transcribe(self, audio):
        # returns 1 alternative by default
        results = self.speech_to_text.recognize(audio).result['results']
        return results[0]['alternatives'][0]['transcript']