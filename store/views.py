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

# token = os.getenv('TOKEN')

# epayco_login_url = os.getenv('EPAYCO_LOGIN_URL')

# epayco_create_link_url = os.getenv('EPAYCO_CREATE_LINK_URL')


# EPAYCO RESPONSE LINKS

# Production
confirmation_url = "https://web-production-aea2.up.railway.app/epayco_confirmation"
response_base_url = "https://web-production-aea2.up.railway.app/epayco_response/"

# Localhost
# confirmation_url = "http://127.0.0.1:8000/epayco_confirmation"
# response_base_url = "http://127.0.0.1:8000/epayco_response/"


# VARIABLES AND FUNCTIONS

from .tools import get_ballot_ids_from_x_description
     
# ePayco_confirmation_time = timedelta(hours=3, minutes=30) 
ePayco_confirmation_time = timedelta(seconds=5) 

def unbind_ballots():
    hopeless_transactions = Transaccion.objects.filter(estado=0).filter(valid_until__lte=timezone.now()-ePayco_confirmation_time)
    for transaction in hopeless_transactions:
        for ballot in transaction.balota_set.all():
            ballot.transaccion = None
            ballot.save()
            
        transaction.estado = 2
        transaction.save()

def handle_transaction_response(data):
    
    x_response = data['x_response']
    transaction = Transaccion.objects.get(id=int(data['x_description'].split(' ')[0]))
    transaction.x_description = data['x_description']
    transaction.x_ref_payco = data['x_ref_payco']
    transaction.valor_pagado = int(data['x_amount'])
    transaction.x_response = x_response
    
    transaction.save()
    
    if transaction.estado == 0:
        
        if x_response == 'Aceptada':
            transaction.estado = 1
          
    elif transaction.estado == 1:
        pass
        
    elif transaction.estado == 2:
        
        if x_response == 'Aceptada':
            
            late_confirmation = EpaycoLateConfirmation(transaccion=transaction, datos_json=json.dumps(data))
            unavailable_ballot_ids = []
            
            ballots = [Balota.objects.get(id=id) for id in get_ballot_ids_from_x_description(data['x_description'])]
            for ballot in ballots:
                
                if ballot.transaccion == None:
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
        
        elif x_response == 'Rechazada':
            pass
        
    transaction.save()
 

# VIEWS  
        
class BalotaListView(ListView):
    model = Balota
    
def balotas(request):
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
            # print('1, valid form')
            client = form.save()
        else:
            # print('1, incomplete form')
            return JsonResponse({
                'errors': [(key, value[0]['message']) for key, value in json.loads(form.errors.as_json()).items()]
            })
        
        value_1 = 0
        ballots = [Balota.objects.get(id=int(id)) for id in body['ballot_ids']]
        for ballot in ballots:
            value_1 += ballot.precio
        
        # print('2,', value_1)
        
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

        # print('4, all ballots were available', )        
        
        transaction = Transaccion(cliente=client, descuento=discount, valor_inicial=value_1, valor_final = value_2)
        transaction.save()
        # transaction_id = transaction.id
        
        # print('5, transaction saved')
        
        for ballot in ballots:
            transaction.balota_set.add(ballot)
            transaction.valid_until = transaction.created_at + ballot.time_period
        
        if value_2 == 0:
            context = {'ballots': ballots, 'client': client}
            # print('6, ballots for free')
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
            # print('6, ballots are not for free')
            
            # Login request
            url = epayco_login_url
            payload = ""
            headers = {
                'Authorization': 'Basic ' + token,
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            given_token = response.json()['token']
            # print('7, first request is done')

            # Create payment link request
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
              "mateo_data": f"parametro opcional{transaction.id}",
            })
            
            headers = {
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer '+ given_token
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            # print('8, second request is done')
            link = response.json()['data']['routeLink'] # if value_1 is 0 change transaction status to efectuada (2)
                                                        # and link to response page.
            transaction.link_de_pago = link
            transaction.save()
            # print(link)
            # print('9, we made it to the response part')

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

def epayco_response(request, transaction_id):   # For the client
    
    if not 'ref_payco' in request.GET.dict().keys():    
        transaction = Transaccion.objects.get(id=transaction_id)
        if transaction.estado == 1:
            message = f"¡Felicidades {transaction.cliente.nombre}! Has adquirido las siguientes balotas:"
            context = {'transaction': transaction, 'message': message}
            return render(request, 'store/response.html', context)
        
        # delete this after testing
        
        # if transaction.estado == 2:
        #     data = {
        #     'x_ref_payco': 'XXXYYYYYXXX', 
        #     'x_description': "105 Compra de balotas. Numeros 8, 13, 14", 
        #     'x_amount': "10000", 
        #     'x_response': "Aceptada"
        #     }
        
        #     handle_transaction_response(data)
            
        #     print('Done!')
            
        #     response = HttpResponse()
        #     response.status_code = 200
        #     return response
        
        # _______________________________________
    
    else:
        encoded_ref_payco = request.GET.dict()['ref_payco']
        url = 'https://secure.epayco.co/validation/v1/reference/' + encoded_ref_payco
        response = requests.request("GET", url)
        data = response.json()['data']
        
        handle_transaction_response(data)
        
        transaction = Transaccion.objects.get(id=int(data['x_description'].split(' ')[0]))
        
        if transaction.estado == 0:
            message = 'La transacción se encuentra en estado pediente, por favor recarga la pagina en unos segundos.'
        elif transaction.estado == 1:
            message = f'¡Felicidades {transaction.cliente.nombre}! Has adquirido las siguientes balotas:'
        elif transaction.estado == 2:
            message = 'La transacción no se ha llevado a cabo con éxito, por favor inténtalo nuevamente.'
            
        context = {'message': message, 'transaction': transaction}
        return render(request, 'store/response.html', context)

@csrf_exempt # Not necessary for GET requests
def epayco_confirmation(request):   # For us
    print('_'*20)
    print('request.GET.dict()', request.GET.dict())
    print('request.method', request.method)
    
    data = {
        'x_ref_payco': request.GET.dict()['x_ref_payco'], 
        'x_description': request.GET.dict()['x_description'], 
        'x_amount': request.GET.dict()['x_amount'], 
        'x_response': request.GET.dict()['x_response']
    }
   
    handle_transaction_response(data)
    
    print('Done!')
    
    response = HttpResponse()
    response.status_code = 200
    return response

