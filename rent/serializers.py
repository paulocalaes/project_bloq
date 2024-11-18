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
        instances = []
        for data in validated_data:
            instance = Rent(**data)
            instance.full_clean()
            instance.save()
            instances.append(instance)
        return instances