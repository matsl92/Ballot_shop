from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from datetime import timedelta
        
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    celular = PhoneNumberField()
    
    def __str__(self):
        return self.nombre
    
class Descuento(models.Model):
    opciones_de_estado = [(True, 'Habilitado'), (False, 'Inhabilitado')]
    PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
    
    estado = models.BooleanField(choices=opciones_de_estado, default=True)
    codigo = models.CharField(max_length=100)
    porcentaje = models.DecimalField(max_digits=3, decimal_places=0, validators=PERCENTAGE_VALIDATOR)
    
    def __str__(self):
        return ''.join([str(self.porcentaje), '%'])
    
class Transaccion(models.Model):
    opciones_de_estado = [(0, 'Pendiente'), (1, 'Efectuada'), (2, 'Vencida')]
    
    estado = models.IntegerField(choices=opciones_de_estado, default=0)
    cliente = models.OneToOneField(Cliente, on_delete=models.DO_NOTHING, default=None, null=True)
    descuento = models.ForeignKey(Descuento, on_delete=models.SET_DEFAULT, default=None, null=True)
    link_de_pago = models.CharField(max_length=100, default=None, null=True)
    valor_inicial = models.IntegerField(default=None, null=True)
    valor_final = models.IntegerField(validators=[MinValueValidator(0)], default=None, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(default=None, null=True)
    ref_epayco = models.CharField(max_length=100, default=None, null=True)
    
class Balota(models.Model):
    numero = models.IntegerField(unique=True)
    precio = models.IntegerField(default=10000)
    seleccionada = models.BooleanField(default=False)
    transaccion = models.ForeignKey(Transaccion, on_delete=models.SET_DEFAULT, default=None, null=True)
    time_period = models.DurationField(default=(timedelta(seconds=30)))
    
    def __str__(self):
        return str(self.numero)
    
class EpaycoConfirmation(models.Model):
    post = models.TextField()
