from django.db import models

class Bloq(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.title

