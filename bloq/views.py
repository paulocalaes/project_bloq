'''
Views module for managing Bloq entities and their associated Lockers.
'''
from typing import Any, Type
from django.db.models import QuerySet
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from locker.models import Locker
from locker.serializers import LockerSerializer
from .models import Bloq
from .serializers import BloqSerializer, BloqListSerializer

class StandardResultsSetPagination(PageNumberPagination):
    '''
    Standard pagination class for Bloq views.

    This pagination class sets the default page size to 10 items per page,
    allows clients to set a custom page size using the 'page_size' query parameter,
    and limits the maximum page size to 100 items.
    '''
    page_size: int = 10
    page_size_query_param: str = 'page_size'
    max_page_size: int = 100

class BloqBulkCreateView(generics.ListCreateAPIView):
    '''
    API view to list all Bloqs or create multiple Bloqs.

    - **GET**: Returns a paginated list of all Bloq instances.
    - **POST**: Allows bulk creation of multiple Bloq instances.
    '''
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    queryset = Bloq.objects.all().order_by('id')

    def get_serializer_class(self) -> Type[BloqSerializer]:
        '''
        Return the appropriate serializer class based on the request method.

        Returns:
            BloqListSerializer if the request method is POST,
            otherwise BloqSerializer.
        '''
        if self.request.method == 'POST':
            return BloqListSerializer
        return BloqSerializer

    @swagger_auto_schema(
        responses={200: BloqSerializer(many=True)}
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests to list all Bloqs.

        Returns:
            A paginated list of Bloq instances.
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=BloqListSerializer,
        responses={201: BloqSerializer(many=True)}
    )
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle POST requests to create multiple Bloqs.

        Accepts:
            A list of Bloq data for bulk creation.

        Returns:
            The created Bloq instances.
        """
        return super().post(request, *args, **kwargs)

class BloqDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a specific Bloq instance.

    - **GET**: Retrieve a Bloq by its ID.
    - **PUT**: Update a Bloq instance.
    - **DELETE**: Delete a Bloq instance.
    """
    queryset = Bloq.objects.all().order_by('id')
    serializer_class = BloqSerializer
    permission_classes = [IsAuthenticated]
    lookup_field: str = 'id'

    @swagger_auto_schema(
        responses={200: BloqSerializer}
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests to retrieve a Bloq instance by ID.

        Returns:
            The requested Bloq instance.
        """
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=BloqSerializer,
        responses={200: BloqSerializer}
    )
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle PUT requests to update a Bloq instance.

        Accepts:
            Updated data for the Bloq instance.

        Returns:
            The updated Bloq instance.
        """
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={204: None}
    )
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle DELETE requests to delete a Bloq instance.

        Returns:
            An empty response with HTTP status 204 (No Content).
        """
        return super().delete(request, *args, **kwargs)

class BloqLockersListView(generics.ListAPIView):
    """
    API view to list all Lockers associated with a specific Bloq.

    Retrieves all Locker instances that belong to the Bloq identified by the provided ID.
    """
    serializer_class = LockerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self) -> QuerySet:
        """
        Get the queryset of Lockers for the specified Bloq.

        Validates that the Bloq ID is provided and exists.

        Raises:
            ValidationError: If Bloq ID is not provided.
            NotFound: If the Bloq does not exist.

        Returns:
            QuerySet of Locker instances belonging to the Bloq.
        """
        bloq_id = self.kwargs.get('id')
        if not bloq_id:
            raise ValidationError("Bloq ID is required.")
        if not Bloq.objects.filter(id=bloq_id).exists():
            raise NotFound("Bloq not found.")
        return Locker.objects.filter(bloqId=bloq_id).order_by('id')

    @swagger_auto_schema(
        responses={200: LockerSerializer(many=True)}
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests to list all Lockers of a specific Bloq.

        Returns:
            A paginated list of Locker instances.
        """
        return super().get(request, *args, **kwargs)

class BloqLockerAvailableView(generics.ListAPIView):
    """
    API view to list all available Lockers of a specific Bloq.

    Retrieves all Locker instances that are not occupied and belong to the specified Bloq.
    """
    serializer_class = LockerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self) -> QuerySet:
        """
        Get the queryset of available Lockers for the specified Bloq.

        Validates that the Bloq ID is provided and exists.

        Raises:
            ValidationError: If Bloq ID is not provided.
            NotFound: If the Bloq does not exist.

        Returns:
            QuerySet of available Locker instances.
        """
        bloq_id = self.kwargs.get('id')
        if not bloq_id:
            raise ValidationError("Bloq ID is required.")
        if not Bloq.objects.filter(id=bloq_id).exists():
            raise NotFound("Bloq not found.")
        return Locker.objects.filter(bloqId=bloq_id, isOccupied=False).order_by('id')

    @swagger_auto_schema(
        responses={200: LockerSerializer(many=True)}
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests to list all available Lockers of a specific Bloq.

        Returns:
            A paginated list of available Locker instances.
        """
        return super().get(request, *args, **kwargs)

class BloqLockerOccupiedView(generics.ListAPIView):
    """
    API view to list all occupied Lockers of a specific Bloq.

    Retrieves all Locker instances that are occupied and belong to the specified Bloq.
    """
    serializer_class = LockerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self) -> QuerySet:
        """
        Get the queryset of occupied Lockers for the specified Bloq.

        Validates that the Bloq ID is provided and exists.

        Raises:
            ValidationError: If Bloq ID is not provided.
            NotFound: If the Bloq does not exist.

        Returns:
            QuerySet of occupied Locker instances.
        """
        bloq_id = self.kwargs.get('id')
        if not bloq_id:
            raise ValidationError("Bloq ID is required.")
        if not Bloq.objects.filter(id=bloq_id).exists():
            raise NotFound("Bloq not found.")
        return Locker.objects.filter(bloqId=bloq_id, isOccupied=True).order_by('id')

    @swagger_auto_schema(
        responses={200: LockerSerializer(many=True)}
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Handle GET requests to list all occupied Lockers of a specific Bloq.

        Returns:
            A paginated list of occupied Locker instances.
        """
        return super().get(request, *args, **kwargs)
