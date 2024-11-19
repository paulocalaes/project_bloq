'''
Module for the Bloq views.
'''
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from locker.models import Locker
from locker.serializers import LockerSerializer
from .models import Bloq
from .serializers import BloqSerializer, BloqListSerializer

class StandardResultsSetPagination(PageNumberPagination):
    '''
    Standard pagination for the Bloq views.
    '''
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BloqBulkCreateView(generics.ListCreateAPIView):
    '''
    List all Bloqs or create multiple Bloqs.'''
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    queryset = Bloq.objects.all().order_by('id')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BloqListSerializer
        return BloqSerializer

    @swagger_auto_schema(
        operation_description="Return the list of all Bloqs.",
        responses={200: BloqSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        # pagination
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create multiples Bloqs",
        request_body=BloqListSerializer,
        responses={201: BloqSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class BloqDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Retrieve, update or delete a Bloq instance.'''
    queryset = Bloq.objects.all().order_by('id')
    serializer_class = BloqSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="Return the Bloq instance.",
        responses={200: BloqSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update the Bloq instance.",
        request_body=BloqSerializer,
        responses={200: BloqSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete the Bloq instance.",
        responses={204: None}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class BloqLockersListView(generics.ListAPIView):
    '''
    List all lockers of a specific Bloq.
    '''
    serializer_class = LockerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        bloq_id = self.kwargs.get('id')
        if not bloq_id:
            raise ValidationError("Bloq ID is required.")
        if not Bloq.objects.filter(id=bloq_id).order_by('id').exists():
            raise NotFound("Bloq not found.")
        return Locker.objects.filter(bloqId=bloq_id).order_by('id')

    @swagger_auto_schema(
        operation_description="Return the list of all lockers of a Bloq.",
        responses={200: LockerSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
class BloqLockerAvailableView(generics.ListAPIView):
    '''
    List all available lockers of a Bloq.'''
    serializer_class = LockerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        bloq_id = self.kwargs.get('id')
        is_occupied = False
        return Locker.objects.filter(bloqId=bloq_id, isOccupied=is_occupied).order_by('id')

    @swagger_auto_schema(
        operation_description="Return the list of all available lockers of a Bloq.",
        responses={200: LockerSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class BloqLockerOccupiedView(generics.ListAPIView):
    '''
    List all occupied lockers of a Bloq.'''
    serializer_class = LockerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        bloq_id = self.kwargs.get('id')
        is_occupied = True
        return Locker.objects.filter(bloqId=bloq_id, isOccupied=is_occupied).order_by('id')

    @swagger_auto_schema(
        operation_description="Return the list of all occupied lockers of a Bloq.",
        responses={200: LockerSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
