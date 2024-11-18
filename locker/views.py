from rest_framework import generics
from .models import Locker
from .serializers import LockerSerializer

class LockerListCreate(generics.ListCreateAPIView):
    queryset = Locker.objects.all()
    serializer_class = LockerSerializer


