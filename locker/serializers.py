"""
Serializers for the Locker model.

This module contains serializers for the Locker model, including a standard serializer
and a list serializer for handling bulk operations.
"""

from typing import List, Dict, Any
from django.db import transaction
from rest_framework import serializers
from .models import Locker


class LockerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Locker model.

    This serializer handles the serialization and deserialization of Locker instances.
    It includes all fields of the Locker model.
    """

    class Meta:
        """
        Meta class for LockerSerializer.

        Specifies the model to serialize and the fields to include.
        """
        model = Locker
        fields = '__all__'


class LockerListSerializer(serializers.ListSerializer):
    """
    List serializer for handling multiple Locker instances.

    This serializer allows for bulk creation and update of Locker instances.
    """

    child = LockerSerializer()

    @transaction.atomic
    def create(self, validated_data: List[Dict[str, Any]]) -> List[Locker]:
        """
        Create multiple Locker instances.

        Args:
            validated_data (List[Dict[str, Any]]): A list of dictionaries containing 
            validated data for each Locker.

        Returns:
            List[Locker]: A list of newly created Locker instances.
        """
        instances: List[Locker] = []
        for data in validated_data:
            instance = Locker(**data)
            instance.full_clean()
            instance.save()
            instances.append(instance)
        return instances

    @transaction.atomic
    def update(self, instances: List[Locker], validated_data: List[Dict[str, Any]]) -> List[Locker]:
        """
        Update multiple Locker instances.

        Args:
            instances (List[Locker]): A list of existing Locker instances to update.
            validated_data (List[Dict[str, Any]]): A list of dictionaries containing 
            validated data for each Locker.

        Returns:
            List[Locker]: A list of updated Locker instances.
        """
        # Map existing instances by their ID for quick lookup
        instance_mapping = {instance.id: instance for instance in instances}
        ret: List[Locker] = []

        for data in validated_data:
            locker_id = data.get('id')
            instance = instance_mapping.get(locker_id)
            if instance is None:
                # Create a new instance if it does not exist
                new_instance = self.child.create(data)
                ret.append(new_instance)
            else:
                # Update the existing instance
                updated_instance = self.child.update(instance, data)
                ret.append(updated_instance)
        return ret
