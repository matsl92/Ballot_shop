import json
import requests
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView
from .forms import ClienteForm
from .models import Cliente, Balota, Transaccion, Descuento, EpaycoConfirmation
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

ePayco_time = timedelta(seconds=10)  # 120 segundos o más

def unbind_ballots():
    hopeless_transactions = Transaccion.objects.filter(estado=0).filter(valid_until__lte=timezone.now()-ePayco_time)
    for transaction in hopeless_transactions:
        for ballot in transaction.balota_set.all():
            ballot.transaccion = None
            ballot.save()
            
        transaction.estado = 2
        transaction.save()
        
class BalotaListView(ListView):
    model = Balota
    
def balotas(request):
    unbind_ballots()
    # hacer login en ePayco
    context = {'object_list': Balota.objects.filter(transaccion=None)}
    return render(request, 'store/balota_list.html', context)

def datos_personales(request):
    if request.method == 'POST':
        # print(request.POST)
        print(str(request.POST))
        # d = dict(request.POST)
        # a = request.POST.copy()
        # a['name'] = 'Mateo'
        # print(a)
        # print(d)
        # for key, value in dict(request.POST).items():
        #     print(key, value)
        balota_ids = dict(request.POST).get('id')
        # print(type(balota_ids))
        # print(balota_ids)
        form = ClienteForm()
        context = {'form': form, 'balota_ids': balota_ids}
        return render(request, 'store/personal_data.html', context)

def cuenta(request):

    if request.method=='POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            client = form.save()
        else:
            messages.error(request, form.errors)
            return redirect('store:balotas')
        
        value_1 = 0
        ballots = [Balota.objects.get(id=id) for id in dict(request.POST).get('balota_id')]
        for ballot in ballots:
            value_1 += ballot.precio
            
        value_2 = value_1
        discount_code = dict(request.POST).get('discount_code')[0]
        discount = None
        if discount_code != '':
            if discount_code in [discount.codigo for discount in Descuento.objects.filter(estado=True)]:
                discount = Descuento.objects.get(codigo=discount_code)
                value_2 = int(value_1 * (1 - discount.porcentaje/100))
                messages.success(request, f'El código es válido, se aplicó un descuento del {discount.porcentaje}%.')
            else:
                messages.warning(request, 'El código de descuento no es válido, por favor inténtalo nuevamente o continua con el valor original de la compra.')
        
        context = {'value_1': value_1, 'value_2': value_2, 'ballots': ballots, 'client': client, 'discount': discount}
        return render(request, 'store/bill.html', context)

def confirmacion(request, *args, **kwargs):
    print(request.POST)
    if request.method == 'POST':
        
        value_1 = int(dict(request.POST).get('value_1')[0])
        value_2 = int(dict(request.POST).get('value_2')[0]) 
        client = Cliente.objects.get(id=dict(request.POST).get('client_id')[0])
        ballots = [Balota.objects.get(id=id) for id in dict(request.POST).get('ballot_id')]
        try:
            discount = Descuento.objects.get(id=dict(request.POST).get('discount_id')[0])
        except:
            discount = None
        
        for ballot in ballots:
            if ballot.transaccion != None:
                messages.error(request, 'Lo sentimos. Alguna de las balotas ya fue vendida, por favor haga su selección nuevamente.')
                return redirect('store:balotas')
        
        transaccion = Transaccion(cliente=client, descuento=discount, valor_inicial=value_1, valor_final = value_2)
        transaccion.save()
        
        for ballot in ballots:
            transaccion.balota_set.add(ballot)
            # if transaccion.valid_until == None or transaccion.created_at + ballot.time_period > transaccion.valid_until:
            #     transaccion.valid_until = transaccion.created_at + ballot.time_period
            transaccion.valid_until = transaccion.created_at + ballot.time_period
        
        if value_2 == 0:
            context = {'ballots': ballots, 'client': client}
            return render(request, 'store/response.html', context)
        
        
        
        else: 
            
            # First request
            url = "https://apify.epayco.co/login/mail"
            token = 'bWF0ZW9zYWxhemFyOTdAaG90bWFpbC5jb206TG1tY21zYjkyXw=='
            payload = ""
            headers = {
                'Authorization': 'Basic ' + token,
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            token = response.json()['token']
            
            # return HttpResponse('When a man lies he murders some part of the world')

            # Second request
            url = "https://apify.epayco.co/collection/link/create"
            dt = timezone.now() + timedelta(minutes=1)
            # print(dt)
            # print('The Date:_____________', dt.strftime('%Y-%m-%d %H:%M:%S'))
            payload = json.dumps({
              "quantity": 1,
              "onePayment": True,
              "amount": str(value_2),
              "currency": "COP",
              "id": 0,  # Debe ser único, si se envia cero, epayco genera uno automaticamente
              "base": "0",
              "description": ", ".join([str(ballot.id) for ballot in ballots]),
              "title": "Link de cobro",
              "typeSell": "2",
            #   "tax": "0", # try with integers instead of strings, 1 for email payment, 2 for via link, 3 via mobile SMS, 4 via social networks
            # "typeSell": 2, 
              "email": client.correo,
              
              "urlConfirmation": "https://web-production-aea2.up.railway.app/epayco_confirmation/",
              "methodConfirmation": "POST",
              "urlResponse": "https://web-production-aea2.up.railway.app/epayco_response/", 
            #   "expirationDate": "2023-03-04 23:35:00"
              "expirationDate": timezone.localtime(transaccion.valid_until).strftime('%Y-%m-%d %H:%M:%S')    # Format Date Time UTC payment link expiration date
              
            })
            headers = {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer '+ token
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
            link = response.json()['data']['routeLink']
            transaccion.link_de_pago = link
            transaccion.save()
            return redirect(link)

@csrf_exempt
def epayco_confirmation(request):   # For us
    
    if request.method == 'POST':
        ballot_ids = []
        epayco_conf = EpaycoConfirmation(post=str(request.POST))
        epayco_conf.save()
        context = {'ballots': [], 'client': None}
        return render(request, 'store/response.html', context)

def epayco_response(request):   # For the client
    print(request.method)
    print(request.GET)
    # client = Cliente.objects.get(id=dict(request.POST).get('client_id')[0])
    # ballots = [Balota.objects.get(id=id) for id in dict(request.POST).get('ballot_id')] 
    # context = {'ballots': ballots, 'client': client}
    return render(request, 'store/response.html', {})