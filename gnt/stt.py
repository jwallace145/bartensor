'''
Speech-to-text adapter and implementing classes.
'''
from django.conf import settings

# from google.cloud import speech
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class STT:
    def __init__(self):
        raise NotImplementedError('Speech-to-text adapter not implemented')

    def transcribe(self, audio):
        raise NotImplementedError(
            'transcribe() not implemented in speech-to-text adapter')


class IBM(STT):
    def __init__(self):
        api_key = getattr(settings, 'WATSON_SPEECH_TO_TEXT_API_KEY', None)

        authenticator = IAMAuthenticator(api_key)
        self.speech_to_text = SpeechToTextV1(authenticator=authenticator)

        self.speech_to_text.set_service_url(
            'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/678b9838-b572-44d3-a3c1-66cf47ce9d67')

    def transcribe(self, audio):
        # returns 1 alternative by default
        try:
            results = self.speech_to_text.recognize(audio).result['results']
            return results[0]['alternatives'][0]['transcript']
        except:
            return 'Could not understand. Try our most popular drink: White Russian'


class Google(STT):
    def __init__(self):
        self.client = speech.SpeechClient()

    def transcribe(self, audio):
        config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.OGG_OPUS,
            language_code='en-US',
            # 8000, 12000, 16000, 24000, and 48000 all fail, the only ones allowed for ogg
            sample_rate_hertz=8000,
            # we know its ogg cause printing the blob in the javascript console tells us the mime type is "audio/ogg"
        )
        recognition_audio = speech.types.RecognitionAudio(content=audio.read())
        results = self.client.recognize(config, recognition_audio).results
        print(results)
        print(dir(results))
        print(type(results))
        return results[0].alternatives[0]
