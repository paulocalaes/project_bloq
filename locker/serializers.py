from rest_framework import serializers
from .models import Locker
from django.db import transaction


class LockerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locker
        fields = '__all__'


class LockerListSerializer(serializers.ListSerializer):
    child = LockerSerializer()

    @transaction.atomic
    def create(self, validated_data):
        locker_objects = [Locker(**item) for item in validated_data]
        return Locker.objects.bulk_create(locker_objects)
