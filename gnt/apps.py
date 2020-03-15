"""
Apps Module
"""

# import necessary modules
from django.apps import AppConfig


class GntConfig(AppConfig):
    """
    Gnt Configuration Class
    """

    name = 'gnt'

    def ready(self):
        import gnt.signals
