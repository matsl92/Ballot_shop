from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ComplexClientSerializer, BalotaSerializer
from store.models import ComplexClient, Balota, Descuento

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
    return Response(serializer.data)

@api_view(['GET'])
def code_validation(request):
    discount_code = request.GET.dict()['discount_code']
    ballot_ids = [int(i) for i in request.GET.dict()['bId'].split(',')]
    if discount_code in [
        discount.discount_code for discount in Descuento.objects.filter(
            lottery=Balota.objects.get(id=ballot_ids[0]).lottery
        ).filter(status=True)
    ]:
        discount = Descuento.objects.get(discount_code=discount_code)
        return Response({
            'percentage': discount.percentage, 
            'status': discount.status
        })
    else:
        return Response({
            'error': 'El código es invalido'
        })