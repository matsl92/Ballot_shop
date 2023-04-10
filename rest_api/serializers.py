from rest_framework import serializers
from store.models import ComplexClient

class ComplexClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplexClient
        fields = '__all__'