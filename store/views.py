import json
import requests
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView
from .forms import ClienteForm
from .models import Cliente, Balota, Transaccion, Descuento, EpaycoConfirmation
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.forms.models import model_to_dict
from django.urls import reverse
from urllib.parse import urlencode


# VARIABLES AND FUNCTIONS

token = 'bWF0ZW9zYWxhemFyOTdAaG90bWFpbC5jb206TG1tY21zYjkyXw=='

ePayco_confirmation_time = timedelta(seconds=120)  # 120 segundos o más

def unbind_ballots():
    hopeless_transactions = Transaccion.objects.filter(estado=0).filter(valid_until__lte=timezone.now()-ePayco_confirmation_time)
    for transaction in hopeless_transactions:
        for ballot in transaction.balota_set.all():
            ballot.transaccion = None
            ballot.save()
            
        transaction.estado = 2
        transaction.save()
 
# VIEWS  
        
class BalotaListView(ListView):
    model = Balota
    
def balotas(request):
    str_values = {'name': 'mateo', 'id': '32', 'age': '25'}
    base_url = reverse('store:balotas')
    str_values['option'] = '1'
    query_string = urlencode(str_values)
    url = '{}?{}'.format(base_url, query_string)
    # return redirect(url)
    print(url)
    unbind_ballots()
    context = {'object_list': Balota.objects.filter(transaccion=None)}
    return render(request, 'store/balota_list.html', context)

def datos_personales(request):
    if request.method == 'POST':
        # print(str(request.POST))
        balota_ids = dict(request.POST).get('id')
        form = ClienteForm()
        context = {'form': form, 'balota_ids': balota_ids}
        return render(request, 'store/personal_data.html', context)

def cuenta(request):
    
    if request.method == 'GET':
        data = {'name': 'Mateo', 'edad': 25}
        return JsonResponse(data)

    if request.method=='POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            client = form.save()
        else:
            messages.error(request, form.errors)
            return redirect('store:balotas') # wrong page
        
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
        ballots = [Balota.objects.get(id=id) for id in dict(request.POST).get('ballot_id')[0].split(',')]
        # ballots = [Balota.objects.get(id=id) for id in dict(request.POST).get('ballot_id')]
        
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
        transaction_id = transaccion.id
        
        for ballot in ballots:
            transaccion.balota_set.add(ballot)
            transaccion.valid_until = transaccion.created_at + ballot.time_period
        
        if value_2 == 0:
            context = {'ballots': ballots, 'client': client}
            return render(request, 'store/response.html', context)
        
        
        
        else: 
            
            # First request
            url = "https://apify.epayco.co/login/mail"
            # token = 'bWF0ZW9zYWxhemFyOTdAaG90bWFpbC5jb206TG1tY21zYjkyXw=='
            payload = ""
            headers = {
                'Authorization': 'Basic ' + token,
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            token = response.json()['token']

            # Second request
            url = "https://apify.epayco.co/collection/link/create"
            payload = json.dumps({
              "quantity": 1,
              "onePayment": True,
              "amount": str(value_2),
              "currency": "COP",
              "id": 0,  # Debe ser único, si se envia cero, epayco genera uno automaticamente
              "base": "0",
              "description": ", ".join([str(ballot.id) for ballot in ballots]),
              "title": "Link de cobro",
              "typeSell": "2", # 1 for email payment, 2 for via link, 3 via mobile SMS, 4 via social networks
              "tax": "0", 
              "email": client.correo,
            #   "urlConfirmation": "https://web-production-aea2.up.railway.app/epayco_confirmation",
              "urlConfirmation": "http://127.0.0.1:8000/epayco_confirmation",
              "methodConfirmation": "GET",
            #   "urlResponse": "https://web-production-aea2.up.railway.app/epayco_response/", 
              "urlResponse": "http://127.0.0.1:8000/epayco_response/{}/".format(transaction_id),
              "expirationDate": timezone.localtime(transaccion.valid_until).strftime('%Y-%m-%d %H:%M:%S')    # Format Date Time UTC payment link expiration date 
            })
            headers = {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer '+ token
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            link = response.json()['data']['routeLink']
            transaccion.link_de_pago = link
            transaccion.save()
            return redirect(link)

@csrf_exempt
def epayco_confirmation(request):   # For us
    print('_'*20)
    print('request.GET.dict()', request.GET.dict())
    print('request.method', request.method)
    x_description = request.GET.dict()['x_description'] # Our description
    x_ref_payco = request.GET.dict()['x_ref_payco'] # for detail request
    transaction_id = request.GET.dict('x_extra1') # Our transaction id
    ballot_ids = request.GET.dict('x_extra2') # ballot ids
    x_response = request.GET.dict()['x_response'] # Aceptada/Rechazada
    x_customer_email = request.GET.dict('x_customer_email') # email entered in epayco
    x_customer_movil = request.GET.dict('x_customer_movil') # phone entered in epayco
    transaction = Transaccion.objects.get(id=transaction_id)
    transaction.x_ref_payco = x_ref_payco
    transaction.x_response = x_response
    transaction.x_description = x_description
    if x_response == 'Aceptada':
        transaction.estado = 1
    elif x_response == 'Rechazada':
        transaction.estado = 2
        
    
    
    
    
    
    transaction.save()
    
    if request.method == 'POST':
        print('ESTO ES POST')
        ballot_ids = []
        epayco_conf = EpaycoConfirmation(post=str(request.POST))
        epayco_conf.save()
        context = {'ballots': [], 'client': None}
        return render(request, 'store/response.html', context)
    if request.method == 'GET':
        print('Esto es get')
    return HttpResponse('confirmación epayco')

def epayco_response(request, transaction_id):   # For the client
    transaction = Transaccion.objects.get(id=transaction_id)
    client = transaction.cliente
    
    if transaction.estado == 0:
        message = 'La transacción se encuentra en estado pediente, por favor recarga la pagina en unos segundos.'
    elif transaction.estado == 1:
        message = f'¡Felicidades {client.nombre}! Has adquirido las siguientes balotas.'
    elif transaction.estado == 2:
        message = 'El link de pago ha vencido, por favor intentalo nuevamente.'
        
    context = {'client': client, 'message': message, 'transaction': transaction}
    return render(request, 'store/response.html', context)

def code_validation(request):
    print('validation request')
    discunt_code = json.loads(request.body)['discount_code']
    print('discount code:', discunt_code)
    if discunt_code in [discount.codigo for discount in Descuento.objects.filter(estado=True)]:
        discount = Descuento.objects.get(codigo=discunt_code)
        return JsonResponse({
            'percentage': discount.porcentaje, 
            'status': discount.estado
        })
    else:
        return JsonResponse({
            'error': 'El código es invalido'
        })

def fetch_api(request):
    if request.method=='POST':
        body = json.loads(request.body)
        form = ClienteForm(body)
        if form.is_valid():
            print('1, valid form')
            client = form.save()
        else:
            print('1, incomplete form')
            return JsonResponse({
                'errors': [(key, value[0]['message']) for key, value in json.loads(form.errors.as_json()).items()]
            })
        
        value_1 = 0
        ballots = [Balota.objects.get(id=int(id)) for id in body['ballot_ids']]
        for ballot in ballots:
            value_1 += ballot.precio
        
        print('2,', value_1)
        
        value_2 = value_1
        discount_code = body['discount_code']
        discount = None
        discount_id = None
        if discount_code != '':
            if discount_code in [discount.codigo for discount in Descuento.objects.filter(estado=True)]:
                discount = Descuento.objects.get(codigo=discount_code)
                discount_id = discount.id
                value_2 = int(value_1 * (1 - discount.porcentaje/100))
                print('3, valid code: ', value_2)
                messages.success(request, f'El código es válido, se aplicó un descuento del {discount.porcentaje}%.')
            else:
                messages.warning(request, 'El código de descuento no es válido, por favor inténtalo nuevamente o continua con el valor original de la compra.')
                print('3, invalid code:', value_2)
        
        for ballot in ballots:
            if ballot.transaccion != None:
                print('4, not all ballots were available')
                messages.error(request, 'Lo sentimos. Alguna de las balotas ya fue vendida, por favor haga su selección nuevamente.')
                return redirect('store:balotas') # this redirect should send the user and not just the fetch request

        print('4, all ballots were available', )        
        
        transaction = Transaccion(cliente=client, descuento=discount, valor_inicial=value_1, valor_final = value_2)
        transaction.save()
        # transaction_id = transaction.id
        
        print('5, transaction saved')
        
        for ballot in ballots:
            transaction.balota_set.add(ballot)
            transaction.valid_until = transaction.created_at + ballot.time_period
        
        # if value_2 == 0:
        #     context = {'ballots': ballots, 'client': client}
        #     print('6, ballots for free')
        #     return render(request, 'store/response.html', context) # return link with client id to response page
        
        
        else: 
            print('6, ballots are not for free')
            
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
            print('7, first request is done')

            # Second request
            url = "https://apify.epayco.co/collection/link/create"
            payload = json.dumps({
              "quantity": 1,
              "onePayment": True,
              "amount": str(value_2),
              "currency": "COP",
              "id": 0,  # Debe ser único, si se envia cero, epayco genera uno automaticamente
              "base": "0",
              "description": f"Compra de balotas con los números: {', '.join([str(ballot.numero) for ballot in ballots])}",
              "title": "Link de cobro",
              "typeSell": "2", # 1 for email payment, 2 for via link, 3 via mobile SMS, 4 via social networks
              "tax": "0", 
              "email": client.correo,
              "x_extra1": transaction.id,
              "x_extra2": ", ".join([str(ballot.id) for ballot in ballots]),
            #   "urlConfirmation": "https://web-production-aea2.up.railway.app/epayco_confirmation",
              "urlConfirmation": "http://127.0.0.1:8000/epayco_confirmation",
              "methodConfirmation": "GET",
            #   "urlResponse": "https://web-production-aea2.up.railway.app/epayco_response/", 
              "urlResponse": "http://127.0.0.1:8000/epayco_response/{}/".format(transaction.id),
              "expirationDate": timezone.localtime(transaction.valid_until).strftime('%Y-%m-%d %H:%M:%S')    # Format Date Time UTC payment link expiration date 
            })
            headers = {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer '+ token
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print('8, second request is done')
            link = response.json()['data']['routeLink'] # if value_1 is 0 change transaction status to efectuada (2)
                                                        # and link to response page.
            transaction.link_de_pago = link
            transaction.save()
            print(link)
            print('9, we made it to the response part')

            return JsonResponse({
                'value_1': value_1, 
                'value_2': value_2, 
                'client': {
                    'name': client.nombre, 
                    'lastname': client.apellido, 
                    'email': client.correo,  
                    'id': client.id
                }, 
                'ballot_ids': [ballot.id for ballot in ballots], 
                'discount_id': discount_id, 
                'link': link
            })
            # return render(request, 'store/bill.html', context)
