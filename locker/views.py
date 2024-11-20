"""
Views for the Locker app.

This module contains API views for managing Locker instances, including listing,
creating multiple lockers, retrieving, updating, and deleting individual lockers,
as well as listing available lockers with optional filtering.
"""

import logging
from typing import Any, Type
from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .serializers import LockerSerializer, LockerListSerializer
from .models import Locker, LockerStatus

# Set up logging
logger = logging.getLogger(__name__)


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class for Locker views.

    This class sets default pagination settings:
    - Default page size is 10 items.
    - Allows clients to set a custom page size using the 'page_size' query parameter.
    - Maximum page size is capped at 100 items.
    """
    page_size: int = 10
    page_size_query_param: str = 'page_size'
    max_page_size: int = 100


class LockerBulkCreateView(generics.ListCreateAPIView):
    """
    API view to list all Lockers or create multiple Lockers at once.

    - **GET**: Returns a paginated list of all Locker instances.
    - **POST**: Allows bulk creation of multiple Locker instances.
    """
    queryset = Locker.objects.all().order_by('id')
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self) -> Type[Serializer]:
        """
        Return the appropriate serializer class based on the request method.

        Returns:
            - LockerListSerializer: For POST requests (bulk creation).
            - LockerSerializer: For GET requests (list all lockers).
        """
        if self.request.method == 'POST':
            return LockerListSerializer
        return LockerSerializer

    @swagger_auto_schema(
        responses={200: LockerSerializer(many=True)}
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests to list all Lockers.

        Returns:
            - Response: A paginated list of Locker instances.
        """
        logger.info("User '%s' requested a list of all Lockers.", request.user.id)
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=LockerListSerializer,
        responses={201: LockerSerializer(many=True)}
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle POST requests to create multiple Lockers.

        Returns:
            - Response: The created Locker instances.
        """
        logger.info("User '%s' is creating multiple Lockers.", request.user.id)
        response = super().post(request, *args, **kwargs)
        logger.info("User '%s' successfully created Lockers.", request.user.id)
        return response


class LockerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific Locker instance.

    - **GET**: Retrieve a Locker by its ID.
    - **PUT**: Update a Locker instance.
    - **DELETE**: Delete a Locker instance.
    """
    queryset = Locker.objects.all()
    serializer_class = LockerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field: str = 'id'

    @swagger_auto_schema(
        responses={200: LockerSerializer}
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests to retrieve a Locker instance by ID.

        Returns:
            - Response: The requested Locker instance.
        """
        locker_id = kwargs.get('id')
        logger.info("User '%s' requested Locker with ID '%s'.", request.user.id, locker_id)
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=LockerSerializer,
        responses={200: LockerSerializer}
    )
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle PUT requests to update a Locker instance.

        Returns:
            - Response: The updated Locker instance.
        """
        locker_id = kwargs.get('id')
        logger.info("User '%s' is updating Locker with ID '%s'.", request.user.id, locker_id)
        response = super().put(request, *args, **kwargs)
        logger.info(
            "User '%s' successfully updated Locker with ID '%s'.", request.user.id, locker_id
            )
        return response

    @swagger_auto_schema(
        responses={204: None}
    )
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle DELETE requests to delete a Locker instance.

        Returns:
            - Response: An empty response with HTTP status 204 (No Content).
        """
        locker_id = kwargs.get('id')
        logger.info("User '%s' is deleting Locker with ID '%s'.", request.user.id, locker_id)
        response = super().delete(request, *args, **kwargs)
        logger.info(
            "User '%s' successfully deleted Locker with ID '%s'.", request.user.id, locker_id
            )
        return response


class AvailableLockerListView(generics.ListAPIView):
    """
    API view to retrieve a list of available Lockers.

    This view allows clients to retrieve a paginated list of Lockers that are available
    (not occupied and open), with optional filtering by Bloq ID ('bloqId') and locker size ('size').

    - **GET**: Returns a paginated list of available Locker instances.
    """
    queryset = Locker.objects.all()
    serializer_class = LockerSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['bloqId', 'size']
    ordering_fields = ['id']

    def get_queryset(self) -> QuerySet:
        """
        Get the queryset of available Lockers.

        Filters Lockers that are not occupied and have status OPEN.
        Allows optional filtering by 'bloqId' and 'size' query parameters.

        Returns:
            - QuerySet: Filtered queryset of available Lockers.
        """
        queryset = super().get_queryset()
        queryset = queryset.filter(isOccupied=False, status=LockerStatus.OPEN).order_by('id')

        bloq_id = self.request.query_params.get('bloqId', None)
        size = self.request.query_params.get('size', None)

        if bloq_id:
            queryset = queryset.filter(bloqId=bloq_id)
            logger.info(
                "User '%s' filtered Lockers by Bloq ID '%s'.", self.request.user.id, bloq_id
                )
        if size:
            queryset = queryset.filter(size=size)
            logger.info("User '%s' filtered Lockers by size '%s'.", self.request.user.id, size)

        logger.info("User '%s' requested available Lockers.", self.request.user.id)
        return queryset

    @swagger_auto_schema(
        responses={200: LockerSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'bloqId',
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
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests to retrieve a list of available Lockers.

        Returns:
            - Response: A paginated list of available Locker instances.
        """
        return super().get(request, *args, **kwargs)
