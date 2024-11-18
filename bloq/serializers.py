'''
This file contains the serializers for the Bloq model.
'''
from rest_framework import serializers
from django.db import transaction
from .models import Bloq

class BloqSerializer(serializers.ModelSerializer):
    '''
    Bloq serializer
    '''
    class Meta:
        '''
        Meta class for BloqSerializer
        '''
        model = Bloq
        fields = '__all__'

class BloqListSerializer(serializers.ListSerializer):
    '''
    Bloq list serializer
    '''
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

    @transaction.atomic
    def update(self, instance, validated_data):
        # Assuming validated_data is a list of dictionaries
        instance_mapping = {inst.id: inst for inst in instance}
        ret = []
        for data in validated_data:
            inst = instance_mapping.get(data.get('id'), None)
            if inst is None:
                ret.append(self.child.create(data))
            else:
                ret.append(self.child.update(inst, data))
        return ret
    