from django.db import models

from bloq.models import Bloq

class LockerStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    CLOSED = 'CLOSED', 'Closed'

class Locker(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    bloq = models.ForeignKey(Bloq, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=LockerStatus.choices)
    isOccupied = models.BooleanField()

    def __str__(self):
        return f"Locker {self.id} - {self.status}"
