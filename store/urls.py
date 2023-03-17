from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('balotas/', views.balotas, name='balotas'), 
    path('datos_personales/', views.datos_personales, name='datos_personales'), 
    path('epayco_confirmation', views.epayco_confirmation, name="epayco_confirmation"),
    path('epayco_response/<int:transaction_id>', views.epayco_response, name="epayco_response"),
    path('bill/', views.fetch_api, name='fetch'), 
    path('code_validation/', views.code_validation, name='code_validation'), 
]
    
    
    
    
    