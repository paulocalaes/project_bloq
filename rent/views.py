from rest_framework import generics
from .models import Rent
from .serializers import RentSerializer

class RentListCreate(generics.ListCreateAPIView):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer

