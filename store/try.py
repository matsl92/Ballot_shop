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

created_at = datetime(2023, 3, 4, 10)

valid_until = created_at + timedelta(seconds=30)

ePayco_time = timedelta(seconds=10)

# dt = datetime(2023, 3, 4, 9, 50)
# for i in range(20):
#   if dt 
#   dt += timedelta(minutes=5)
  
print(created_at < valid_until)


# print(created_at.strftime('%Y-%m-%d %H:%M:%S'))
print(created_at.strftime('%d/%m/%Y %H:%M'))
print(created_at.strftime('%Y-%m-%d %H:%M:%S'))