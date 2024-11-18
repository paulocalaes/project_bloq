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
        bloq_objects = [Bloq(**item) for item in validated_data]
        return Bloq.objects.bulk_create(bloq_objects)
