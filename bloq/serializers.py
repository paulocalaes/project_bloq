from rest_framework import serializers
from .models import Bloq
from django.db import transaction

class BloqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloq
        fields = '__all__'

class BloqListSerializer(serializers.ListSerializer):
    child = BloqSerializer()

    @transaction.atomic
    def create(self, validated_data):
        instances = []
        for data in validated_data:
            instance = Bloq(**data)
            instance.full_clean() 
            instance.save()
            instances.append(instance)
        return instances