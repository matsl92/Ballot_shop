from django.urls import path
from . import views

urlpatterns = [
    path('first_endpoint/', views.get_data), 
    path('get_ballots', views.get_ballots), 
    path('code_validation', views.code_validation), 
]