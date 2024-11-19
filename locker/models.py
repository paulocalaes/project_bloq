'''
models.py
'''
from django.db import models

from bloq.models import Bloq

class LockerStatus(models.TextChoices):
    '''
    Locker status choices
    '''
    OPEN = 'OPEN', 'Open'
    CLOSED = 'CLOSED', 'Closed'

class LockerSize(models.TextChoices):
    '''
    Locker size choices
    '''
    XS = 'XS', 'Extra Small'
    S = 'S', 'Small'
    M = 'M', 'Medium'
    L = 'L', 'Large'
    XL = 'XL', 'Extra Large'


class Locker(models.Model):
    '''
    Locker model
    '''
    id = models.CharField(max_length=255, primary_key=True)
    bloqId = models.ForeignKey(Bloq, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=LockerStatus.choices)
    isOccupied = models.BooleanField()
    size = models.CharField(max_length=2, choices=LockerSize.choices, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return f"Locker {self.id} - {self.status}"
