from django.db import models

from locker.models import Locker

class RentStatus(models.TextChoices):
    CREATED = 'CREATED', 'Created'
    WAITING_DROPOFF = 'WAITING_DROPOFF', 'Waiting Dropoff'
    WAITING_PICKUP = 'WAITING_PICKUP', 'Waiting Pickup'
    DELIVERED = 'DELIVERED', 'Delivered'

class RentSize(models.TextChoices):
    XS = 'XS', 'Extra Small'
    S = 'S', 'Small'
    M = 'M', 'Medium'
    L = 'L', 'Large'
    XL = 'XL', 'Extra Large'

class Rent(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    locker = models.ForeignKey(Locker, on_delete=models.CASCADE)
    weight = models.FloatField()
    size = models.CharField(max_length=2, choices=RentSize.choices)
    status = models.CharField(max_length=20, choices=RentStatus.choices)

    def __str__(self):
        return f"Rent {self.id} - {self.status}"
