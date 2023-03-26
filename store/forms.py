from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['first_name', 'last_name', 'email', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'field__input', 'id': 'first-name'
                }),
            'last_name': forms.TextInput(attrs={
                'class': 'field__input', 'id': 'last-name'
                }),
            'email': forms.EmailInput(attrs={
                'class': 'field__input', 'id': 'email'
                }),
            'phone_number': forms.TextInput(attrs={
                'class': 'field__input', 'id': 'phone-number'
                }), 
        }