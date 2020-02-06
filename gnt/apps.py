from django.apps import AppConfig


class GntConfig(AppConfig):
    name = 'gnt'

    def ready(self):
        import gnt.signals
