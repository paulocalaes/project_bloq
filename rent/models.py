'''
This file contains the model for the Rent object.
'''
from django.db import models
from locker.models import Locker,LockerSize

class RentStatus(models.TextChoices):
    '''
    Enum for Rent status
    '''
    CREATED = 'CREATED', 'Created'
    WAITING_DROPOFF = 'WAITING_DROPOFF', 'Waiting Dropoff'
    WAITING_PICKUP = 'WAITING_PICKUP', 'Waiting Pickup'
    DELIVERED = 'DELIVERED', 'Delivered'

class Rent(models.Model):
    '''
    Model for Rent object
    '''
    id = models.CharField(max_length=255, primary_key=True)
    lockerId = models.ForeignKey(Locker, on_delete=models.CASCADE)
    weight = models.FloatField()
    size = models.CharField(max_length=2, choices=LockerSize.choices)
    status = models.CharField(max_length=20, choices=RentStatus.choices)

    objects = models.Manager()

    def __str__(self):
        return f"Rent {self.id} - {self.status}"
