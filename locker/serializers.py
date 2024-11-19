'''
Serializers for Locker model
'''
from django.db import transaction
from rest_framework import serializers
from .models import Locker



class LockerSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Locker model
    '''
    class Meta:
        '''
        Meta class for the LockerSerializer
        '''
        model = Locker
        fields = '__all__'


class LockerListSerializer(serializers.ListSerializer):
    '''
    Serializer for multiple Locker objects
    '''
    child = LockerSerializer()

    @transaction.atomic
    def create(self, validated_data):
        instances = []
        for data in validated_data:
            instance = Locker(**data)
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
