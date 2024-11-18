from rest_framework import generics
from .models import Locker
from .serializers import LockerSerializer, LockerListSerializer
from drf_yasg.utils import swagger_auto_schema

class LockerBulkCreateView(generics.ListCreateAPIView):
    queryset = Locker.objects.all()

    @swagger_auto_schema(
        operation_description="Return the list of all Lockers.",
        responses={200: LockerSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create multiples Lockers",
        request_body=LockerListSerializer,
        responses={201: LockerSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



