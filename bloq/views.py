from rest_framework import generics
from .models import Bloq
from .serializers import BloqSerializer, BloqListSerializer
from drf_yasg.utils import swagger_auto_schema

class BloqBulkCreateView(generics.ListCreateAPIView):
    queryset = Bloq.objects.all()

    @swagger_auto_schema(
        operation_description="Return the list of all Bloqs.",
        responses={200: BloqSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create multiples Bloqs",
        request_body=BloqListSerializer,
        responses={201: BloqSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
