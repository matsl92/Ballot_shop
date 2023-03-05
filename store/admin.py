from django.contrib import admin

from .models import *

admin.site.register([Cliente, Descuento, Transaccion, Balota, EpaycoConfirmation, Rango])
