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
from .models import Cliente, Balota, Transaccion, Descuento, EpaycoLateConfirmation
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.forms.models import model_to_dict
from django.urls import reverse
from urllib.parse import urlencode
import os
from dotenv import load_dotenv


load_dotenv()


# ENVIRONMENT VARIABLES

token = 'bWF0ZW9zYWxhemFyOTdAaG90bWFpbC5jb206TG1tY21zYjkyXw=='

epayco_login_url = 'https://apify.epayco.co/login/mail'

epayco_create_link_url = 'https://apify.epayco.co/collection/link/create'

epayco_transaction_detail_url = 'https://apify.epayco.co/transaction/detail'

# token = os.getenv('TOKEN')

# epayco_login_url = os.getenv('EPAYCO_LOGIN_URL')

# epayco_create_link_url = os.getenv('EPAYCO_CREATE_LINK_URL')

# epayco_transaction_detail_url = os.getenv('EPAYCO_TRANSACTION_DETAIL_URL')


# EPAYCO RESPONSE LINKS

# Production
# confirmation_url = "https://web-production-aea2.up.railway.app/epayco_confirmation"
# response_base_url = "https://web-production-aea2.up.railway.app/epayco_response/"

# Localhost
confirmation_url = "http://127.0.0.1:8000/epayco_confirmation"
response_base_url = "http://127.0.0.1:8000/epayco_response/"


# VARIABLES AND FUNCTIONS

url_base = '//'.join([confirmation_url.split('/')[0], confirmation_url.split('/')[2]])

from .tools import get_ballot_ids_from_x_description
     
# ePayco_confirmation_time = timedelta(hours=3, minutes=30) 
ePayco_confirmation_time = timedelta(seconds=5) 

def epayco_get_token():
    # Login request
    url = epayco_login_url
    payload = ""
    headers = {
        'Authorization': 'Basic ' + token,
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    given_token = response.json()['token']
    return given_token

def epayco_get_transaction_link(value_2, transaction, ballots, client):
    url = epayco_create_link_url
    payload = json.dumps({
        "quantity": 1,
        "onePayment": True,
        "amount": str(value_2),
        "currency": "COP",
        "id": 0,  # Debe ser único, si se envia cero, epayco genera uno automaticamente
        "base": "0",
        "description": f"{transaction.id} Compra de balotas. Numeros: {[ballot.numero for ballot in ballots]}",
        "title": "Link de cobro",
        "typeSell": "2", # 1 for email payment, 2 for via link, 3 via mobile SMS, 4 via social networks
        "tax": "0", 
        "email": client.correo,
        'extra': transaction.id,
        "extra1": transaction.id,
        "extra2": ", ".join([str(ballot.id) for ballot in ballots]),
        "urlConfirmation": confirmation_url, 
        "urlResponse": response_base_url + str(transaction.id), 
        "methodConfirmation": "GET", # request.method = 'POST' anyway
        "expirationDate": timezone.localtime(transaction.valid_until).strftime('%Y-%m-%d %H:%M:%S'),    # Format Date Time UTC payment link expiration date 
    })
    
    headers = {
        'Content-Type': 'application/json', 
        'Authorization': 'Bearer '+ epayco_get_token()
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    link = response.json()['data']['routeLink']
    return link

def epayco_get_transaction_details(x_ref_payco):
    url = epayco_transaction_detail_url

    payload = json.dumps({
    "filter": {
        "referencePayco": int(x_ref_payco)
    }
    })
    headers = {
    'Content-Type': 'application/json', 
    'Authorization': 'Bearer '+ epayco_get_token()
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    return response.json()['data']

def unbind_ballots():
    hopeless_transactions = Transaccion.objects.filter(estado=0).filter(valid_until__lte=timezone.now()-ePayco_confirmation_time)
    for transaction in hopeless_transactions:
        for ballot in transaction.balota_set.all():
            ballot.transaccion = None
            ballot.save()
            
        transaction.estado = 2
        transaction.save()

def handle_transaction_response(data):
    
    # data comes from a simple request for epayco_response
    # but comes from an epayco request for epayco_confirmation since
    # we don't have the encoded_ref_payco
    
    x_response = data['x_response']
    transaction = Transaccion.objects.get(id=int(data['x_description'].split(' ')[0]))
    transaction.x_description = data['x_description']
    transaction.x_ref_payco = data['x_ref_payco']
    transaction.valor_pagado = int(data['x_amount'])
    transaction.x_response = x_response
    
    transaction.save()
    
    if transaction.estado == 0:
        
        if transaction.x_response == 'Pendiente':
            pass
        elif transaction.x_response == 'Rechazada':
            pass
        elif transaction.x_response == 'Fallida':
            pass
        elif transaction.x_response == 'Aceptada':
            transaction.estado = 1
    
    
    elif transaction.estado == 1:
        pass
    
    
    elif transaction.estado == 2:
        if transaction.x_response == 'Pendiente':
            pass
        elif transaction.x_response == 'Rechazada':
            pass
        elif transaction.x_response == 'Fallida':
            pass
        elif transaction.x_response == 'Aceptada':
            
            # late confirmation
            late_confirmation = EpaycoLateConfirmation(
                transaccion=transaction, datos_json=json.dumps(data)
            )
        
            unavailable_ballot_ids = []
            
            ballots = [
                Balota.objects.get(id=id) for id in get_ballot_ids_from_x_description(
                    data['x_description']
                )
            ]
            for ballot in ballots:
                
                if ballot.transaccion == None or ballot.transaccion == transaction:
                    ballot.transaccion = transaction
                    ballot.save()
                
                else:
                    transaction.late_confirmation = timezone.now()
                    late_confirmation.estado = 1
                    unavailable_ballot_ids.append(ballot.id)
            
            description = {'unavailable_ballot_ids': unavailable_ballot_ids}
            late_confirmation.descripcion = json.dumps(description)
            transaction.estado = 1
            late_confirmation.save() 
    
    
    transaction.save()
    
    
# VIEWS  
        
class BalotaListView(ListView):
    model = Balota

def template(request):
    return render(request, 'index.html', {})

def home(request):
    return render(request, 'store/home.html', {})
    
def balotas(request):
    unbind_ballots()
    ballots = list(Balota.objects.all())
    ballot_package = []
    count = 0
    for c in range(6):
        col = []
        for r in range(3):
            col.append(ballots[count])
            count +=1
        ballot_package.append(col)
    print(ballot_package)
    
    ballot_package = list(Balota.objects.all())[0:15]
    
    
                
        
    context = {'object_list': Balota.objects.filter(transaccion=None), 'ballot_package': ballot_package}
    return render(request, 'store/balota_list.html', context)

def datos_personales(request):
    if request.method == 'POST':
        balota_ids = dict(request.POST).get('id')
        form = ClienteForm()
        context = {'form': form, 'balota_ids': balota_ids}
        return render(request, 'store/personal_data.html', context)

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
            client = form.save()
        else:
            return JsonResponse({
                'errors': [(key, value[0]['message']) for key, value in json.loads(form.errors.as_json()).items()]
            })
        
        value_1 = 0
        ballots = [Balota.objects.get(id=int(id)) for id in body['ballot_ids']]
        for ballot in ballots:
            value_1 += ballot.precio
        value_2 = value_1
        discount_code = body['discount_code']
        discount = None
        discount_id = None
        if discount_code != '':
            if discount_code in [discount.codigo for discount in Descuento.objects.filter(estado=True)]:
                discount = Descuento.objects.get(codigo=discount_code)
                discount_id = discount.id
                value_2 = int(value_1 * (1 - discount.porcentaje/100))
                # print('3, valid code: ', value_2)
                # messages.success(request, f'El código es válido, se aplicó un descuento del {discount.porcentaje}%.')
            else:
                # messages.warning(request, 'El código de descuento no es válido, por favor inténtalo nuevamente o continua con el valor original de la compra.')
                print('3, invalid code:', value_2)
        
        for ballot in ballots:
            if ballot.transaccion != None:
                print('4, not all ballots were available')
                # messages.error(request, 'Lo sentimos. Alguna de las balotas ya fue vendida, por favor haga su selección nuevamente.')
                return redirect('store:balotas') # this redirect should send the user and not just the fetch request       
        
        transaction = Transaccion(cliente=client, descuento=discount, valor_inicial=value_1, valor_final = value_2)
        transaction.save()
        
        for ballot in ballots:
            transaction.balota_set.add(ballot)
            transaction.valid_until = transaction.created_at + ballot.time_period
        
        if value_2 == 0:
            context = {'ballots': ballots, 'client': client}
            transaction.estado = 1
            transaction.save()
            link = reverse('store:epayco_response', kwargs={'transaction_id': transaction.id})
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
            return render(request, 'store/response.html', context) # return link with client id to response page
        
        
        else: 
            
            link = epayco_get_transaction_link(value_2, transaction, ballots, client)
            transaction.link_de_pago = link
            transaction.save()

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

def epayco_response(request, transaction_id):   # For the client
     
    transaction = Transaccion.objects.get(id=transaction_id)
    
    if not transaction.link_de_pago:  
        if transaction.estado == 1:
            context = {'transaction': transaction}
            return render(request, 'store/response.html', context)
        
    else:
        encoded_ref_payco = request.GET.dict()['ref_payco']
        url = 'https://secure.epayco.co/validation/v1/reference/' + encoded_ref_payco
        response = requests.request("GET", url)
        data = response.json()['data']
        data['view_link'] = ''.join([url_base, request.get_full_path()])
        
        handle_transaction_response(data)
        
        transaction = Transaccion.objects.get(id=int(data['x_description'].split(' ')[0]))
        
        context = {'transaction': transaction, 'data':data}
        
        return render(request, 'store/response.html', context)

@csrf_exempt
def epayco_confirmation(request):
    print('_'*20)

    x_ref_payco = request.POST.dict()['x_ref_payco']
    
    data = epayco_get_transaction_details(x_ref_payco)
    
    data['x_ref_payco'] = data['referencePayco']
    data['x_response'] = data['status']
    data['x_description'] = data['description']
    data['x_amount'] = data['amount']
    
    handle_transaction_response(data)
    
    response = HttpResponse()
    
    response.status_code = 200
    
    print('Doneee!')
    return response
       
def transaction_detail(request, x_ref_payco):
     
    return JsonResponse(epayco_get_transaction_details(x_ref_payco))
