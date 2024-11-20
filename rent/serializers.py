"""
Serializers for the Rent model.

This module contains serializers for the Rent model, including a standard serializer
and a list serializer for handling bulk operations.
"""

from typing import List, Dict, Any
from django.db import transaction
from rest_framework import serializers
from .models import Rent


class RentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rent model.

    This serializer handles the serialization and deserialization of Rent instances.
    It includes all fields of the Rent model.
    """

    class Meta:
        """
        Meta class for RentSerializer.

        Specifies the model to serialize and the fields to include.
        """
        model = Rent
        fields = '__all__'


class RentListSerializer(serializers.ListSerializer):
    """
    List serializer for handling multiple Rent instances.

    This serializer allows for bulk creation and update of Rent instances.
    """

    child = RentSerializer()

    @transaction.atomic
    def create(self, validated_data: List[Dict[str, Any]]) -> List[Rent]:
        """
        Create multiple Rent instances.

        Args:
            validated_data (List[Dict[str, Any]]): A list of dictionaries containing 
            validated data for each Rent.

        Returns:
            List[Rent]: A list of newly created Rent instances.
        """
        instances: List[Rent] = []
        for data in validated_data:
            instance = Rent(**data)
            instance.full_clean()
            instance.save()
            instances.append(instance)
        return instances

    @transaction.atomic
    def update(self, instances: List[Rent], validated_data: List[Dict[str, Any]]) -> List[Rent]:
        """
        Update multiple Rent instances.

        Args:
            instances (List[Rent]): A list of existing Rent instances to update.
            validated_data (List[Dict[str, Any]]): A list of dictionaries containing 
            validated data for each Rent.

        Returns:
            List[Rent]: A list of updated Rent instances.
        """
        # Map existing instances by their ID for quick lookup
        instance_mapping = {instance.id: instance for instance in instances}
        ret: List[Rent] = []

        for data in validated_data:
            rent_id = data.get('id')
            instance = instance_mapping.get(rent_id)
            if instance is None:
                # Create a new instance if it does not exist
                new_instance = self.child.create(data)
                ret.append(new_instance)
            else:
                # Update the existing instance
                updated_instance = self.child.update(instance, data)
                ret.append(updated_instance)
        return ret
