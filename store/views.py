import json
import requests
import math
from datetime import timedelta, datetime, date
from django.utils import timezone
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView
from .forms import ClienteForm
from .models import Cliente, Balota, Transaccion, Descuento, EpaycoLateConfirmation, Rifa, Sociedad
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .strings import message_mapper 
import os
from dotenv import load_dotenv


load_dotenv()


# ENVIRONMENT VARIABLES

society_id = int(os.getenv('SOCIETY_ID'))

token = os.getenv('TOKEN')

epayco_login_url = os.getenv('EPAYCO_LOGIN_URL')

epayco_create_link_url = os.getenv('EPAYCO_CREATE_LINK_URL')

epayco_transaction_detail_url = os.getenv('EPAYCO_TRANSACTION_DETAIL_URL')


# EPAYCO RESPONSE LINKS

base_url = f"http{os.getenv('HTTP_SAFE')}://{os.getenv('DOMAIN')}{os.getenv('LOCAL_PORT')}"

confirmation_url = f"{base_url}/epayco_confirmation"

response_base_url = f"{base_url}"


# VARIABLES AND FUNCTIONS

society_creation_date = date(2018, 2, 6)

try:
    society = Sociedad.objects.get(id=society_id)
except:
    society = None

url_base = '//'.join([confirmation_url.split('/')[0], confirmation_url.split('/')[2]])

from .tools import (
    make_transaction_description, 
    get_values_from_transaction_description, 
    get_percentage_to_display
)
     
ePayco_confirmation_time = timedelta(hours=3, minutes=30)

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
        "description": make_transaction_description(ballots, transaction), 
        "title": "Link de cobro",
        "typeSell": "2", # 2 via link
        "tax": "0", 
        "urlConfirmation": confirmation_url, 
        "urlResponse": response_base_url + '?tr_pk=' + str(transaction.id), 
        "methodConfirmation": "GET", # request.method = 'POST' anyway ?tr_id=
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

def unbind_ballots(lottery):
    
    # hopeless_transactions = Transaccion.objects.filter(estado=0).filter(valid_until__lte=timezone.now()-ePayco_confirmation_time)
    # for transaction in hopeless_transactions:
    #     for ballot in transaction.balota_set.all():
    #         ballot.transaccion = None
    #         ballot.save()
            
    #     transaction.estado = 2
    #     transaction.save()
    
    
    lottery_ballots = list(Balota.objects.filter(lottery=lottery))
    lottery_transactions = []
    for ballot in lottery_ballots:
        if ballot.transaction != None and not ballot.transaction in lottery_transactions:
            lottery_transactions.append(ballot.transaction)
    hopeless_transactions = []
    for transaction in lottery_transactions:
        if transaction.status == 0 and transaction.valid_until < timezone.now()-ePayco_confirmation_time:
            hopeless_transactions.append(transaction)
    for transaction in hopeless_transactions:
        for ballot in transaction.balota_set.all():
            ballot.transaction = None
            ballot.save()
            
        transaction.status = 2
        transaction.save()

def handle_transaction_response(data):
    
    """
    Epayco_response gets data from a simple request 
    but epayco_confirmation makes a more complex process since it doesn't
    have that encoded ref_payco
    """
    
    purchase_details = get_values_from_transaction_description(data['x_description'])
    x_response = data['x_response']
    transaction = Transaccion.objects.get(id=purchase_details['transaction_id'])
    transaction.x_description = data['x_description']
    transaction.x_ref_payco = data['x_ref_payco']
    transaction.validated_value = int(data['x_amount'])
    transaction.x_response = x_response
    
    transaction.save()
    
    if transaction.status == 0:
        
        if transaction.x_response == 'Pendiente':
            pass
        elif transaction.x_response == 'Rechazada':
            pass
        elif transaction.x_response == 'Fallida':
            pass
        elif transaction.x_response == 'Aceptada':
            transaction.status = 1
    
    
    elif transaction.status == 1:
        pass
    
    
    elif transaction.status == 2:
        if transaction.x_response == 'Pendiente':
            pass
        elif transaction.x_response == 'Rechazada':
            pass
        elif transaction.x_response == 'Fallida':
            pass
        elif transaction.x_response == 'Aceptada':
            
            # late confirmation
            late_confirmation = EpaycoLateConfirmation(
                transaction=transaction, json_data=json.dumps(data)
            )
        
            unavailable_ballot_ids = []
            
            ballots = [Balota.objects.get(id=id) for id in purchase_details['ballot_ids']]
            
            for ballot in ballots:
                
                if ballot.transaction == None or ballot.transaction == transaction:
                    ballot.transaction = transaction
                    ballot.save()
                
                else:
                    late_confirmation.status = 1
                    unavailable_ballot_ids.append(ballot.id)
            
            description = {'unavailable_ballot_ids': unavailable_ballot_ids}
            late_confirmation.description = json.dumps(description)
            transaction.status = 1
            late_confirmation.save() 
    
    
    transaction.save()
    
    
# VIEWS 

def get_ballots(request):
    body_string = request.body.decode('utf8').replace("'", '"')
    body = json.loads(body_string)
    lottery_id = int(body['lottery_id'])
    lottery = Rifa.objects.get(id=lottery_id)
    ballot_list = list(Balota.objects.filter(lottery=lottery).filter(transaction=None))
    ballots= []
    for ballot in ballot_list:
        ballots.append({'number': ballot.number, 'id': ballot.id, 'checked': False})
    
    return JsonResponse(ballots, safe=False)

def home(request):
    js_variables = {'msg':['', '']}
    
    if 'tr_pk' in request.GET.dict().keys():
        
        """" Epeyco response """
        transaction = Transaccion.objects.get(id=int(request.GET.dict()['tr_pk']))

        if not transaction.payment_link:  
            if transaction.status == 1:
                js_variables['msg'] = message_mapper['Aceptada']
                
        else:
            encoded_ref_payco = request.GET.dict()['ref_payco']
            url = 'https://secure.epayco.co/validation/v1/reference/' + encoded_ref_payco
            response = requests.request("GET", url)
            data = response.json()['data']
            data['view_link'] = ''.join([url_base, request.get_full_path()])
            
            handle_transaction_response(data)
            
            js_variables['msg'] = message_mapper[data['x_response']]
            
            if data['x_response'] == 'Rechazada' or data['x_response'] == 'Fallida':
                js_variables['link'] = transaction.payment_link
    
    if 'msg' in request.GET.dict().keys():
        key = request.GET.dict()['msg']
        js_variables['msg'] = message_mapper[key]
        
    try:
        lottery = society.rifa_set.filter(is_active=True).first()
    except:
        lottery = None
    
    js_variables['lottery_id'] = lottery.id
    
    unbind_ballots(lottery)
    
    try:
        js_variables['ballot_price'] = Balota.objects.filter(lottery=lottery).first().price
    except:
        js_variables['ballot_price'] = 1000000
    
    js_variables['ballot_fetch_url'] = f"{base_url}/fetch_ballots/"
    
    
        
    
    context = {
        'js_variables': js_variables, 
        'years_on_dutty': (datetime.now().date() - society_creation_date).days // 365, 
        'days_left_to_play': (lottery.lottery_date - datetime.today().date()).days
    }
    
    if lottery.display_percentage:
        percentage = len(Balota.objects.filter(
                lottery=lottery
            ).filter(transaction__status=1))/len(Balota.objects.filter(
                lottery=lottery
            ))*100
        
        # context['sold_ballot_percentage'] = get_percentage_to_display(percentage)
        
        context['sold_ballot_percentage'] = int(percentage)
    
    return render(request, 'store/index.html', context)
    
def datos_personales(request):
    if request.method == 'POST':
        try:
            balota_ids = dict(request.POST).get('id')
            ballots = [Balota.objects.get(id=id) for id in balota_ids]
            subtotal = 0
            for ballot in ballots:
                subtotal += ballot.price
            js_variables = {
                'bId': balota_ids, 
                'code_validation_url': f"{base_url}/code_validation/", 
                'link_creation_url': f"{base_url}/bill/"
            }
            context = {'js_variables': js_variables, 'ballots': ballots, 'subtotal': subtotal}
            return render(request, 'store/form.html', context)
        except:
            url = reverse('store:home')
            return redirect(url + '?msg=empty')

def code_validation(request):
    discount_code = json.loads(request.body)['discount_code']
    ballot_ids = json.loads(request.body)['bId']
    if discount_code in [
        discount.discount_code for discount in Descuento.objects.filter(
            status=True
        ).filter(lottery=Balota.objects.get(id=ballot_ids[0]).lottery)
    ]:
        discount = Descuento.objects.get(discount_code=discount_code)
        return JsonResponse({
            'percentage': discount.percentage, 
            'status': discount.status
        })
    else:
        return JsonResponse({
            'error': 'El código es invalido'
        })

def fetch_api(request):
    if request.method=='POST':
        body = {
            'first_name': request.POST['first_name'], 
            'last_name': request.POST['last_name'], 
            'email': request.POST['email'], 
            'phone_number': request.POST['phone_number'], 
            'ballot_ids': [int(i) for i in request.POST['ballot_ids'].split(',')], 
            'discount_code': request.POST['discount_code']
        }
        
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
            value_1 += ballot.price
        value_2 = value_1
        discount_code = body['discount_code']
        discount = None
        if discount_code != '':
            if discount_code in [
                discount.discount_code for discount in Descuento.objects.filter(
                    lottery=Balota.objects.get(id=ballots[0].id).lottery
                ).filter(status=True)
            ]:
                discount = Descuento.objects.get(discount_code=discount_code)
                value_2 = int(value_1 * (1 - discount.percentage/100))
        
        for ballot in ballots:
            if ballot.transaction != None:
                messages.error(request, 'Lo sentimos. Alguna de las balotas ya fue vendida, por favor haz tu selección nuevamente.')
                link = reverse('store:home')
                link += '?msg=unavailable'
                return redirect(link)       
        
        transaction = Transaccion(client=client, discount=discount, value_1=value_1, value_2 = value_2)
        transaction.save()
        
        for ballot in ballots:
            transaction.balota_set.add(ballot)
            transaction.valid_until = transaction.created_at + ballot.unavailable_time
        transaction.save()
        
        if value_2 == 0:
            transaction.status = 1
            transaction.save()
            link = reverse('store:home')
            link += '?tr_pk=' + str(transaction.pk)
            return redirect(link)
        
        else: 
            
            link = epayco_get_transaction_link(value_2, transaction, ballots, client)
            transaction.payment_link = link
            transaction.save()
            return redirect(link)

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

def test_view(request):
    
    object_list = []
    for i in range(100):
        object_list.append(i)

    n_ballots = 32
    n_slides = math.ceil(len(object_list)/n_ballots)

    package = []

    
    count = 0
    for i in range(n_slides):
        slide = []
        for j in range(n_ballots):
            slide.append(object_list[count])
            count += 1
            if count == len(object_list):
                break
        package.append(slide)
        
        
            
    context = {'package': package}
    return render(request, 'store/test.html', context)