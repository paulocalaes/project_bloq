from rest_framework import serializers
from .models import Bloq

class BloqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloq
        fields = '__all__'
