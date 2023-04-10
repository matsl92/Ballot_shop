from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ComplexClientSerializer, BalotaSerializer
from store.models import ComplexClient, Balota, Rifa
import json

@api_view(['GET'])
def get_data(request):
    complex_clients = ComplexClient.objects.all()
    serializer = ComplexClientSerializer(complex_clients, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_ballots(request):
    lottery_id = int(request.GET.dict()['lottery_id'])
    ballots = Balota.objects.filter(lottery__id=lottery_id).filter(transaction=None)
    serializer = BalotaSerializer(ballots, many=True)
    print(Response(serializer.data))
    return Response(serializer.data)