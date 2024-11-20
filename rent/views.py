"""
Views for the Rent app.

This module contains API views for managing Rent instances, including listing,
creating multiple rents, handling rent drop-offs, and processing rent pickups.
"""

import logging
from typing import Any, Type
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from drf_yasg.utils import swagger_auto_schema
from locker.models import Locker, LockerStatus
from .models import Rent, RentStatus
from .serializers import RentSerializer, RentListSerializer

# Set up logging
logger = logging.getLogger(__name__)


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
        logger.info("User '%s' requested a list of all Rents.", request.user.id)
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
        logger.info("User '%s' is creating multiple Rents.", request.user.id)
        # Change the status of the lockers to 'OPEN' and 'isOccupied' to False
        for rent_data in request.data:
            locker_id = rent_data['lockerId']
            Locker.objects.filter(id=locker_id).update(status=LockerStatus.OPEN, isOccupied=False)
            rent_data['status'] = RentStatus.WAITING_DROPOFF
            logger.debug("Updated Locker ID '%s' to status OPEN and isOccupied False.", locker_id)
        response = super().post(request, *args, **kwargs)
        logger.info("User '%s' successfully created Rents.", request.user.id)
        return response


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
        rent_id = kwargs.get('id')
        logger.info("User '%s' is processing drop-off for Rent ID '%s'.", request.user.id, rent_id)
        rent = self.get_object()
        locker = rent.lockerId
        locker.status = LockerStatus.CLOSED
        locker.isOccupied = True
        locker.save()
        logger.debug("Updated Locker ID '%s' to status CLOSED and isOccupied True.", locker.id)
        rent.status = RentStatus.WAITING_PICKUP
        rent.save()
        logger.info("Rent ID '%s' status updated to WAITING_PICKUP.", rent_id)
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
        rent_id = kwargs.get('id')
        logger.info("User '%s' is processing pickup for Rent ID '%s'.", request.user.id, rent_id)
        rent = self.get_object()
        locker = rent.lockerId
        locker.status = LockerStatus.OPEN
        locker.isOccupied = False
        locker.save()
        logger.debug("Updated Locker ID '%s' to status OPEN and isOccupied False.", locker.id)
        rent.status = RentStatus.DELIVERED
        rent.save()
        logger.info("Rent ID '%s' status updated to DELIVERED.", rent_id)
        serializer = self.get_serializer(rent)
        return Response(serializer.data)
