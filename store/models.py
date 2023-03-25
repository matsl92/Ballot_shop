from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from datetime import timedelta

class Rifa(models.Model):
    Lottery_date = models.DateField('Fecha de sorteo')
    ballot_price = models.PositiveIntegerField('Precio de las balotas', default=10000)    
    min_number = models.IntegerField('Número mínimo', validators=[MinValueValidator(0)])
    max_number = models.IntegerField('Número máximo', validators=[MinValueValidator(0)])
    step = models.IntegerField('Paso', validators=[MinValueValidator(1)])
    ballot_unavailable_time = models.DurationField('Tiempo de inhabilidad de las balotas')
    prize = models.CharField('Premio', max_length=200)
    
    def save(self):
        n = (self.max_number+1 - self.min_number) // self.step   
        if self.min_number <= self.max_number and n > 0:
            super().save()
            for i in range((self.max_number+1-self.min_number)//self.step):
                if not self.min_number + self.step*i in [
                    ballot.number for ballot in Balota.objects.filter(lottery=self)
                ]:
                    
                    ballot = Balota(
                        number=self.min_number+self.step*i, 
                        price = self.ballot_price, 
                        unavailable_time = self.ballot_unavailable_time, 
                        lottery = self
                    )
                
                    ballot.save()
        
class Cliente(models.Model):
    first_name = models.CharField('Nombre', max_length=100)
    last_name = models.CharField('Apellido', max_length=100)
    email = models.EmailField('Correo electrónico')
    phone_number = PhoneNumberField('Número de celular')
    
    def __str__(self):
        return self.first_name
    
class Descuento(models.Model):
    lottery= models.ForeignKey(Rifa, on_delete=models.CASCADE, verbose_name='Sorteo')
    status_options = [(True, 'Habilitado'), (False, 'Inhabilitado')]
    PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
    status = models.BooleanField('Estado', choices=status_options, default=True)
    discount_code = models.CharField('Código de descuento', max_length=100)
    percentage = models.DecimalField('Porcentaje de descuento', max_digits=3, decimal_places=0, validators=PERCENTAGE_VALIDATOR)
    
    def __str__(self):
        return ''.join([str(self.percentage), '%'])
    
class Transaccion(models.Model):
    status_options = [(0, 'Pendiente'), (1, 'Efectuada'), (2, 'Vencida')]
    
    status = models.IntegerField('Estado', choices=status_options, default=0)
    client = models.OneToOneField(Cliente, on_delete=models.DO_NOTHING, default=None, null=True, blank=True, verbose_name='Cliente')
    discount = models.ForeignKey(Descuento, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True, verbose_name='Descuento')
    payment_link = models.CharField('Link de pago', max_length=100, default=None, null=True, blank=True)
    value_1 = models.IntegerField('Valor inicial', default=None, null=True, blank=True)
    value_2 = models.IntegerField('Valor final', validators=[MinValueValidator(0)], default=None, null=True, blank=True)
    validated_value = models.PositiveIntegerField('Valor validado', default=None, null=True, blank=True)
    created_at = models.DateTimeField('Creado', default=timezone.now)
    valid_until = models.DateTimeField('Válido hasta', default=None, null=True, blank=True)
    x_ref_payco = models.CharField(max_length=100, default=None, null=True, blank=True)
    x_description = models.CharField(max_length=100, default=None, null=True, blank=True)
    x_response = models.CharField(max_length=100, default=None, null=True, blank=True)
    
class Balota(models.Model):
    number = models.IntegerField('Número')
    price = models.PositiveIntegerField('Precio', default=10000)
    selected = models.BooleanField('Seleccionada', default=False)
    transaction = models.ForeignKey(Transaccion, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True, verbose_name='Transacción')
    unavailable_time = models.DurationField('Tiempo de inhabilidad', default=(timedelta(minutes=15)))
    lottery = models.ForeignKey(Rifa, on_delete=models.CASCADE, verbose_name='Sorteo')
    
    def __str__(self):
        return str(self.number)
    
class EpaycoLateConfirmation(models.Model):
    status_options = [(0, 'OK'), (1, 'Por resolver')] 
    
    transaccion = models.OneToOneField(Transaccion, on_delete=models.CASCADE, default=None, null=True)   
    status = models.IntegerField('Estado', choices=status_options, default=0)
    json_data = models.TextField('Datos Json', default='', null=True, blank=True)
    description = models.TextField('Descripción', default='', null=True, blank=True)
    
    def __str__(self):
        return 'Para ' + str(self.transaccion)

# class Rango(models.Model):
#     valor_minimo = models.IntegerField(validators=[MinValueValidator(0)])
#     valor_maximo = models.IntegerField(validators=[MinValueValidator(0)])
#     paso = models.IntegerField(validators=[MinValueValidator(1)])
#     tiempo_de_reserva = models.DurationField()
#     precio = models.IntegerField(validators=[MinValueValidator(0)], default=10000)
    
#     def save(self):
#         n = (self.valor_maximo+1 - self.valor_minimo) // self.paso
#         if self.valor_minimo <= self.valor_maximo and n > 0:
#             super().save()
#             for i in range((self.valor_maximo+1-self.valor_minimo)//self.paso):
                
#                 if not self.valor_minimo + self.paso*i in [
#                     ballot.id for ballot in Balota.objects.all()
#                 ]:
                    
#                     ballot = Balota(
#                     numero=self.valor_minimo+self.paso*i, 
#                     precio = self.precio, 
#                     time_period = self.tiempo_de_reserva
#                     )
                
#                     ballot.save()
                    

                 
                    