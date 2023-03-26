import requests
import json

# # from django.conf import settings

# # settings.configure()
# token = 'bWF0ZW9zYWxhemFyOTdAaG90bWFpbC5jb206TG1tY21zYjkyXw=='
# # test https://logistica.epayco.io/
# url = "https://apify.epayco.co/login/mail"

# payload = ""
# headers = {
#     'Authorization': 'Basic ' + token,
#     # 'Authorization': 'Basic ' + settings.BASIC_AUTH_TOKEN, 
#     'Content-Type': 'application/json', 
#     # 'public_key': 
# }

# response = requests.request("POST", url, headers=headers, data=payload)
# token = response.json()['token']
# print(token)
# print('_'*20)
# # print(response.text)

# # print(' '.join(['bearer', token]))

# url = "https://apify.epayco.co/collection/link/create"

# payload = json.dumps({
#   "quantity": 1,
#   "onePayment": True,
#   "amount": "83500",
#   "currency": "COP",
#   "id": 0,
#   "base": "0",
#   "description": "Link de test",
#   "title": "Link de cobro de prueba",
#   "typeSell": "1",
#   "tax": "0",
#   "email": "felipe.mesa@payco.co"
# })
# headers = {
#   'Content-Type': 'application/json',
#   'Authorization': 'Bearer '+ token
# #   'Authorization': str(''.join(['Bearer', str(token)]))
# }                
# response = requests.request("POST", url, headers=headers, data=payload)
# link = response.json()['data']['routeLink']
# print(link)
# # print(response.text)


from datetime import datetime, timedelta

# created_at = datetime(2023, 3, 4, 10)

# valid_until = created_at + timedelta(seconds=30)

# ePayco_time = timedelta(seconds=10)

# dt = datetime(2023, 3, 4, 9, 50)
# for i in range(20):
#   if dt 
#   dt += timedelta(minutes=5)
  
# print(created_at < valid_until)


# print(created_at.strftime('%Y-%m-%d %H:%M:%S'))
# print(created_at.strftime('%d/%m/%Y %H:%M'))
# print(created_at.strftime('%Y-%m-%d %H:%M:%S'))

# response_base_url = "https://web-production-aea2.up.railway.app/epayco_response/"

# url = response_base_url + str(23) +'/'

# print(url)

# print('Hello world!')

# response = {"success":True,"title_response":"Correcto","text_response":"Transacción consultada existosamente","last_action":"Consultar Transaccion","data":{"x_cust_id_cliente":782193,"x_ref_payco":131834374,"x_id_factura":"78219364127aa2b7217-1678932653988","x_id_invoice":"78219364127aa2b7217-1678932653988","x_description":"94 Compra de balotas. Numeros 8","x_amount":10000,"x_amount_country":10000,"x_amount_ok":10000,"x_tax":0,"x_tax_ico":0,"x_amount_base":0,"x_currency_code":"COP","x_bank_name":"BANCO DE PRUEBAS","x_cardnumber":"457562*******0326","x_quotas":"5","x_respuesta":"Aceptada","x_response":"Aceptada","x_approval_code":"000000","x_transaction_id":"131834374","x_fecha_transaccion":"2023-03-15 21:13:24","x_transaction_date":"2023-03-15 21:13:24","x_cod_respuesta":1,"x_cod_response":1,"x_response_reason_text":"Aprobada","x_cod_transaction_state":1,"x_transaction_state":"Aceptada","x_errorcode":"00","x_franchise":"VS","x_business":"Mateo Salazar","x_customer_doctype":"","x_customer_document":"","x_customer_name":"","x_customer_lastname":"","x_customer_email":"mateosalazar97@hotmail.com","x_customer_phone":"","x_customer_movil":"","x_customer_ind_pais":"","x_customer_country":"","x_customer_city":"","x_customer_address":"","x_customer_ip":"152.202.61.187","x_signature":"d18fe15215b6a6378d3a2f75b17d090b0350898583f355430c3513e081f0ac12","x_test_request":"TRUE","x_transaction_cycle":None,"x_extra1":"","x_extra2":"","x_extra3":"","x_extra4":"","x_extra5":"","x_extra6":"","x_extra7":"","x_extra8":"","x_extra9":"","x_extra10":"","x_type_payment":"TDC"}}
# data = response['data']
# id = int(data['x_description'].split(' ')[0])
# print(id)
# print('hola')

# x_description = "96 Compra de balotas. Numeros 8, 13, 14"
# # x_description = "94 Compra de balotas. Numeros 8"

# items = x_description.split(' ')
# items.pop(0)
# ballot_ids =[]
# for item in items:
#     try:
#         ballot_id = int(item.strip(','))
#         ballot_ids.append(ballot_id)
#     except:
#         pass

# print(ballot_ids)

# dic = {'a':1, 'b': {'er':'hola', 'rfd': 32}}
# string = json.dumps(dic)
# recover_dic = json.loads(string)
# print(type(recover_dic['b']))


# confirmation_url = "http://127.0.0.1:8000/epayco_confirmation"

# print(confirmation_url)

# url_base = '//'.join([confirmation_url.split('/')[0], confirmation_url.split('/')[2]])
# print(url_base)