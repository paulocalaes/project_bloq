'''
This file is used to configure the app name.
'''
from django.apps import AppConfig


class LockerConfig(AppConfig):
    '''
    Configuration for the Locker app
    '''
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'locker'
