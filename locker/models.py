from django.db import models

from bloq.models import Bloq

class LockerStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    CLOSED = 'CLOSED', 'Closed'

class LockerSize(models.TextChoices):
    XS = 'XS', 'Extra Small'
    S = 'S', 'Small'
    M = 'M', 'Medium'
    L = 'L', 'Large'
    XL = 'XL', 'Extra Large'


class Locker(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    bloqId = models.ForeignKey(Bloq, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=LockerStatus.choices)
    isOccupied = models.BooleanField()
    size = models.CharField(max_length=2, choices=LockerSize.choices, null=True, blank=True)

    def __str__(self):
        return f"Locker {self.id} - {self.status}"
