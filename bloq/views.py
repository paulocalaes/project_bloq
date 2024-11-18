from rest_framework import generics
from .models import Bloq
from .serializers import BloqSerializer, BloqListSerializer

class BloqBulkCreateView(generics.ListCreateAPIView):
    queryset = Bloq.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BloqListSerializer
        return BloqSerializer
