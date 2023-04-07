from django.contrib import admin

from .models import *
    
class BalotaAdmin(admin.ModelAdmin):
    list_display = ('number', 'lottery')
    
admin.site.register([
    Cliente, 
    Descuento, 
    Transaccion, 
    EpaycoLateConfirmation, 
    Sociedad, Rifa
])

admin.site.register(Balota, BalotaAdmin)