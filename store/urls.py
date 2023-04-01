from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('', views.home, name='home'), 
    path('datos_personales/', views.datos_personales, name='datos_personales'), 
    path('epayco_confirmation', views.epayco_confirmation, name="epayco_confirmation"),
    path('bill/', views.fetch_api, name='fetch'), 
    path('code_validation/', views.code_validation, name='code_validation'), 
    path('fetch_ballots/', views.get_ballots, name='get_ballots')
]
    
    
    
    
    