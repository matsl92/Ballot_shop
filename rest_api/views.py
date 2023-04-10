from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ComplexClientSerializer
from store.models import ComplexClient

@api_view(['GET'])
def get_data(request):
    complex_clients = ComplexClient.objects.all()
    serializer = ComplexClientSerializer(complex_clients, many=True)
    return Response(serializer.data)