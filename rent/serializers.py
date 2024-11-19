'''
Serializer for Rent model
'''
from rest_framework import serializers
from django.db import transaction
from .models import Rent


class RentSerializer(serializers.ModelSerializer):
    '''
    Serializer for Rent model
    '''
    class Meta:
        '''
        Meta class for RentSerializer
        '''
        model = Rent
        fields = '__all__'



class RentListSerializer(serializers.ListSerializer):
    '''
    Serializer for Rent model
    '''
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

    @transaction.atomic
    def update(self, instance, validated_data):
        # Implement the update logic here
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    