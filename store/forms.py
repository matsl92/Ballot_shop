from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'correo', 'celular']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'field__input', 'id': 'id_nombre', 'placeholder': 'ej: Juan'
                }),
            'apellido': forms.TextInput(attrs={
                'class': 'field__input', 'id': 'id_apellido', 'placeholder': 'ej: Correa'
                }),
            'correo': forms.EmailInput(attrs={
                'class': 'field__input', 'id': 'id_correo', 'placeholder': 'ej: juan33@gmail.com'
                }),
            'celular': forms.TextInput(attrs={
                'class': 'field__input', 'id': 'id_celular', 'placeholder': 'ej: 4003002010'
                }), 
        }