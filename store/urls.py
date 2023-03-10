from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('balotas/', views.balotas, name='balotas'), 
    path('datos_personales/', views.datos_personales, name='datos_personales'), 
    path('cuenta/', views.cuenta, name="cuenta"), 
    path('checkout/', views.confirmacion, name='confirmacion'), 
    path('epayco_confirmation/', views.EpaycoConfirmation, name="epayco_confirmation"), 
    path('epayco_response/', views.epayco_response, name="epayco_response"), 
    path('test/', views.fetch_try, name='fetch')
    
    
    
    
    
    
    
    # path('', views.home, name='home'), 
    # path('checkout/', views.checkout, name='checkout'), 
    # path('epayco/success/', views.success, name='success'), 
    # path('epayco/failure/', views.failure, name='failure'), 
    # path('balotas/', views.BalotaListView.as_view(), name='balotas'), 
]
    
    
    
    
    