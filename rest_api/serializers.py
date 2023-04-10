from rest_framework import serializers
from store.models import ComplexClient, Balota

class ComplexClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplexClient
        fields = '__all__'
        
class BalotaSerializer(serializers.ModelSerializer):
    class Meta:
         model = Balota
         fields = ['number', 'id', 'price']