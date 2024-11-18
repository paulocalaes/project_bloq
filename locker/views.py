from rest_framework import generics
from .models import Locker
from .serializers import LockerSerializer, LockerListSerializer

class LockerBulkCreateView(generics.ListCreateAPIView):
    queryset = Locker.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LockerListSerializer
        return LockerSerializer


