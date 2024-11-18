from rest_framework import generics
from .models import Rent
from .serializers import RentSerializer, RentListSerializer

class RentBulkCreateView(generics.ListCreateAPIView):
    queryset = Rent.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RentListSerializer
        return RentSerializer

