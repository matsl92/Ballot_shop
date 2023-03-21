from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'correo', 'celular']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'field__input', 'id': 'id_nombre', 'placeholder': 'Juan'
                }),
            'apellido': forms.TextInput(attrs={
                'class': 'field__input', 'id': 'id_apellido', 'placeholder': 'Correa'
                }),
            'correo': forms.EmailInput(attrs={
                'class': 'field__input', 'id': 'id_correo', 'placeholder': 'juan33@gmail.com'
                }),
            'celular': forms.TextInput(attrs={
                'class': 'field__input', 'id': 'id_celular', 'placeholder': '4003002010'
                }), 
        }