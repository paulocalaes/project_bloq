'''
Views for the Locker app.
'''
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from .serializers import LockerSerializer, LockerListSerializer
from .models import Locker, LockerStatus

class LockerBulkCreateView(generics.ListCreateAPIView):
    '''
    View for creating multiple Lockers at once.
    '''
    queryset = Locker.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return LockerListSerializer
        return LockerSerializer

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

class LockerDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    View for retrieving detailed information about a specific locker.
    '''
    queryset = Locker.objects.all()
    serializer_class = LockerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="Return the Locker instance.",
        responses={200: LockerSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update the Locker instance.",
        request_body=LockerSerializer,
        responses={200: LockerSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete the Locker instance.",
        responses={204: None}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class AvailableLockerListView(generics.ListAPIView):
    '''
    View for retrieving a list of available lockers.
    '''
    queryset = Locker.objects.all()
    serializer_class = LockerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['bloqId', 'size']
    ordering_fields = ['id']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(isOccupied=False, status=LockerStatus.OPEN)

        bloq_id = self.request.query_params.get('bloqId', None)
        if bloq_id:
            queryset = queryset.filter(bloq__id=bloq_id)
        size = self.request.query_params.get('size', None)
        if size:
            queryset = queryset.filter(size=size)
        return queryset

    @swagger_auto_schema(
        operation_description="Retrieve a list of available lockers.",
        responses={200: LockerSerializer(many=True)},
        manual_parameters=[
           openapi.Parameter(
               'bloq_id', 
               openapi.IN_QUERY,
               description="Filter by Bloq ID",
               type=openapi.TYPE_STRING
            ),
           openapi.Parameter(
               'size', 
               openapi.IN_QUERY,
               description="Filter by locker size",
               type=openapi.TYPE_STRING
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    