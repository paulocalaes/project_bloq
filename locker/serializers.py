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
        instances = []
        for data in validated_data:
            instance = Locker(**data)
            instance.full_clean()
            instance.save()
            instances.append(instance)
        return instances
