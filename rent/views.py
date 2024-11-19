'''
Views for the rent app
'''
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from .models import Rent
from .serializers import RentSerializer, RentListSerializer

class RentBulkCreateView(generics.ListCreateAPIView):
    '''
    View for creating multiple Rents
    '''
    queryset = Rent.objects.all()

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
        return super().post(request, *args, **kwargs)
