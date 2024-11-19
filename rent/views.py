'''
Views for the rent app
'''
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from locker.models import Locker, LockerStatus
from .models import Rent, RentStatus
from .serializers import RentSerializer, RentListSerializer

class StandardResultsSetPagination(PageNumberPagination):
    '''
    Standard pagination for the Bloq views.
    '''
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
class RentBulkCreateView(generics.ListCreateAPIView):
    '''
    View for creating multiple Rents
    '''
    queryset = Rent.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RentListSerializer
        return RentSerializer

    @swagger_auto_schema(
        operation_description="Return the list of all Rents.",
        responses={200: RentSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create multiples Rents",
        request_body=RentListSerializer,
        responses={201: RentSerializer(many=True)}
    )
    def post(self, request, *args, **kwargs):
        # change the status of the locker to occupied
        for rent in request.data:
            locker = rent['lockerId']
            Locker.objects.filter(id=locker).update(status=LockerStatus.OPEN, isOccupied=False)
            rent['status'] = RentStatus.WAITING_DROPOFF
        return super().post(request, *args, **kwargs)

class RentDropoffView(generics.UpdateAPIView):
    '''
    View for dropping off a Rent
    '''
    permission_classes = [IsAuthenticated]
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="Drop off a Rent",
        request_body=RentSerializer,
        responses={200: RentSerializer}
    )
    def patch(self, request, *args, **kwargs):
        rent = Rent.objects.get(id=kwargs['id'])
        locker = rent.lockerId
        locker.status = LockerStatus.CLOSED
        locker.isOccupied = True
        locker.save()
        rent.status = RentStatus.WAITING_PICKUP
        rent.save()
        serializer = self.get_serializer(rent)
        return Response(serializer.data)

class RentPickupView(generics.UpdateAPIView):
    '''
    View for Picking up a Rent
    '''
    permission_classes = [IsAuthenticated]
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="Pick up a Rent",
        request_body=RentSerializer,
        responses={200: RentSerializer}
    )
    def patch(self, request, *args, **kwargs):
        rent = Rent.objects.get(id=kwargs['id'])
        locker = rent.lockerId
        locker.status = LockerStatus.OPEN
        locker.isOccupied = False
        locker.save()
        rent.status = RentStatus.DELIVERED
        rent.save()
        serializer = self.get_serializer(rent)
        return Response(serializer.data)
