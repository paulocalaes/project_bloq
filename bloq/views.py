from rest_framework import generics
from .models import Bloq
from .serializers import BloqSerializer

class BloqListCreate(generics.ListCreateAPIView):
    queryset = Bloq.objects.all()
    serializer_class = BloqSerializer
