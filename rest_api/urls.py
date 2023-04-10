from django.urls import path
from . import views

urlpatterns = [
    path('first_endpoint/', views.get_data, name='get_data'), 
]