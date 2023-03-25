from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'field__input', 'id': 'id_nombre', 'placeholder': 'ej: Juan'
                }),
            'last_name': forms.TextInput(attrs={
                'class': 'field__input', 'id': 'id_apellido', 'placeholder': 'ej: Correa'
                }),
            'email': forms.EmailInput(attrs={
                'class': 'field__input', 'id': 'id_correo', 'placeholder': 'ej: juan33@gmail.com'
                }),
            'phone_number': forms.TextInput(attrs={
                'class': 'field__input', 'id': 'id_celular', 'placeholder': 'ej: 4003002010'
                }), 
        }