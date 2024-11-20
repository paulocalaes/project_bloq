"""
Serializers for the Bloq model.

This module contains serializers for the Bloq model, including a standard serializer
and a list serializer for handling bulk operations.
"""

from typing import List, Dict, Any
from django.db import transaction
from rest_framework import serializers
from .models import Bloq


class BloqSerializer(serializers.ModelSerializer):
    """
    Serializer for the Bloq model.

    This serializer handles the serialization and deserialization of Bloq instances.
    It includes all fields of the Bloq model.
    """

    class Meta:
        """
        Meta class for BloqSerializer.

        Specifies the model to serialize and the fields to include.
        """
        model = Bloq
        fields = '__all__'


class BloqListSerializer(serializers.ListSerializer):
    """
    List serializer for handling multiple Bloq instances.

    This serializer allows for bulk creation and update of Bloq instances.
    """

    child = BloqSerializer()

    @transaction.atomic
    def create(self, validated_data: List[Dict[str, Any]]) -> List[Bloq]:
        """
        Create multiple Bloq instances.

        Args:
            validated_data (List[Dict[str, Any]]): A list of dictionaries containing
              validated data for each Bloq.

        Returns:
            List[Bloq]: A list of newly created Bloq instances.
        """
        instances: List[Bloq] = []
        for data in validated_data:
            instance = Bloq(**data)
            instance.full_clean()
            instance.save()
            instances.append(instance)
        return instances

    @transaction.atomic
    def update(self, instance: List[Bloq], validated_data: List[Dict[str, Any]]) -> List[Bloq]:
        """
        Update multiple Bloq instances.

        Args:
            instance (List[Bloq]): A list of existing Bloq instances to update.
            validated_data (List[Dict[str, Any]]): A list of dictionaries containing 
            validated data for each Bloq.

        Returns:
            List[Bloq]: A list of updated Bloq instances.
        """
        # Map existing instances by their ID for quick lookup
        instance_mapping = {inst.id: inst for inst in instance}
        ret: List[Bloq] = []
        for data in validated_data:
            inst = instance_mapping.get(data.get('id'))
            if inst is None:
                # Create a new instance if it does not exist
                new_instance = self.child.create(data)
                ret.append(new_instance)
            else:
                # Update the existing instance
                updated_instance = self.child.update(inst, data)
                ret.append(updated_instance)
        return ret
