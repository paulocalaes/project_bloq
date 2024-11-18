'''
This file is used to configure the app name.
'''
from django.apps import AppConfig


class BloqConfig(AppConfig):
    '''
    Bloq app configuration
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bloq'
