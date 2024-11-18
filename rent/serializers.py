from rest_framework import serializers
from .models import Rent
from django.db import transaction

class RentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rent
        fields = '__all__'



class RentListSerializer(serializers.ListSerializer):
    child = RentSerializer()

    @transaction.atomic
    def create(self, validated_data):
        rent_objects = [Rent(**item) for item in validated_data]
        return Rent.objects.bulk_create(rent_objects)