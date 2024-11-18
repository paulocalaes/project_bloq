'''
Models for the Bloq app
'''
from django.db import models


class Bloq(models.Model):
    '''
    Bloq model
    '''
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    objects = models.Manager()  # Add this line to define the default manager

    def __str__(self):
        return str(self.title)
