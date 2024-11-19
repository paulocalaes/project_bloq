"""
Views for the Rent app.

This module contains API views for managing Rent instances, including listing,
creating multiple rents, handling rent drop-offs, and processing rent pickups.
"""

from typing import Any, Type
from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from locker.models import Locker, LockerStatus
from .models import Rent, RentStatus
from .serializers import RentSerializer, RentListSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class for Rent views.

    This class sets default pagination settings:
    - Default page size is 10 items.
    - Allows clients to set a custom page size using the 'page_size' query parameter.
    - Maximum page size is capped at 100 items.
    """
    page_size: int = 10
    page_size_query_param: str = 'page_size'
    max_page_size: int = 100


class RentBulkCreateView(generics.ListCreateAPIView):
    """
    API view to list all Rents or create multiple Rents at once.

    - **GET**: Returns a paginated list of all Rent instances.
    - **POST**: Allows bulk creation of multiple Rent instances.
    """
    queryset = Rent.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self) -> Type[RentSerializer]:
        """
        Return the appropriate serializer class based on the request method.

        Returns:
            - RentListSerializer: For POST requests (bulk creation).
            - RentSerializer: For GET requests (list all rents).
        """
        if self.request.method == 'POST':
            return RentListSerializer
        return RentSerializer

    @swagger_auto_schema(
        responses={200: RentSerializer(many=True)}
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests to list all Rents.

        Returns:
            - Response: A paginated list of Rent instances.
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=RentListSerializer,
        responses={201: RentSerializer(many=True)}
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle POST requests to create multiple Rents.

        Updates the status of associated Lockers and sets the Rent status to WAITING_DROPOFF.

        Returns:
            - Response: The created Rent instances.
        """
        # Change the status of the lockers to 'OPEN' and 'isOccupied' to False
        for rent_data in request.data:
            locker_id = rent_data['lockerId']
            Locker.objects.filter(id=locker_id).update(status=LockerStatus.OPEN, isOccupied=False)
            rent_data['status'] = RentStatus.WAITING_DROPOFF
        return super().post(request, *args, **kwargs)


class RentDropoffView(generics.UpdateAPIView):
    """
    API view for processing a Rent drop-off.

    - **PATCH**: Updates the Rent and associated Locker statuses to reflect a drop-off.
    """
    permission_classes = [IsAuthenticated]
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    lookup_field: str = 'id'

    @swagger_auto_schema(
        request_body=RentSerializer,
        responses={200: RentSerializer}
    )
    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle PATCH requests to process a Rent drop-off.

        Updates:
            - Locker status to 'CLOSED' and 'isOccupied' to True.
            - Rent status to 'WAITING_PICKUP'.

        Returns:
            - Response: The updated Rent instance.
        """
        rent_id = kwargs['id']
        rent = self.get_object()
        locker = rent.lockerId
        locker.status = LockerStatus.CLOSED
        locker.isOccupied = True
        locker.save()
        rent.status = RentStatus.WAITING_PICKUP
        rent.save()
        serializer = self.get_serializer(rent)
        return Response(serializer.data)


class RentPickupView(generics.UpdateAPIView):
    """
    API view for processing a Rent pickup.

    - **PATCH**: Updates the Rent and associated Locker statuses to reflect a pickup.
    """
    permission_classes = [IsAuthenticated]
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    lookup_field: str = 'id'

    @swagger_auto_schema(
        request_body=RentSerializer,
        responses={200: RentSerializer}
    )
    def patch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle PATCH requests to process a Rent pickup.

        Updates:
            - Locker status to 'OPEN' and 'isOccupied' to False.
            - Rent status to 'DELIVERED'.

        Returns:
            - Response: The updated Rent instance.
        """
        rent_id = kwargs['id']
        rent = self.get_object()
        locker = rent.lockerId
        locker.status = LockerStatus.OPEN
        locker.isOccupied = False
        locker.save()
        rent.status = RentStatus.DELIVERED
        rent.save()
        serializer = self.get_serializer(rent)
        return Response(serializer.data)
