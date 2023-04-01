from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from datetime import timedelta

class Sociedad(models.Model):
    name = models.CharField('Nombre', max_length=100)
    
    def __str__(self):
        return self.name

class Rifa(models.Model):
    is_active = models.BooleanField('Está activa', default=False)
    society = models.ForeignKey(Sociedad, on_delete=models.CASCADE, verbose_name='Sociedad')
    name = models.CharField('Nombre de la rifa', max_length=100)
    prize = models.CharField('Premio', max_length=200)
    description = models.TextField('Descripción', max_length=1000, blank=True, null=True)
    lottery_date = models.DateField('Fecha de sorteo')
    ballot_price = models.PositiveIntegerField('Precio de las balotas', default=10000)    
    min_number = models.IntegerField('Número mínimo', validators=[MinValueValidator(0)])
    max_number = models.IntegerField('Número máximo', validators=[MinValueValidator(0)])
    step = models.IntegerField('Paso', validators=[MinValueValidator(1)])
    ballot_unavailable_time = models.DurationField('Tiempo de inhabilidad de las balotas', default=timedelta(minutes=10))
    
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
                    
        if self.is_active:
                for lottery in self.society.rifa_set.all():
                    if lottery != self and lottery.is_active:
                        lottery.is_active = False
                        lottery.save()
    
    def __str__(self):
        return self.name
        
class Cliente(models.Model):
    first_name = models.CharField('Nombre', max_length=100)
    last_name = models.CharField('Apellido', max_length=100)
    email = models.CharField('Correo electrónico', max_length=100)
    phone_number = models.PositiveIntegerField('Número de celular')
    
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
    
    def __str__(self):
        return f"Transacción {self.id}"
    
class Balota(models.Model):
    number = models.IntegerField('Número')
    price = models.PositiveIntegerField('Precio', default=10000)
    selected = models.BooleanField('Seleccionada', default=False)
    transaction = models.ForeignKey(Transaccion, on_delete=models.SET_DEFAULT, default=None, null=True, blank=True, verbose_name='Transacción')
    unavailable_time = models.DurationField('Tiempo de inhabilidad', default=(timedelta(minutes=15)))
    lottery = models.ForeignKey(Rifa, on_delete=models.CASCADE, verbose_name='Rifa')
    
    def __str__(self):
        return str(self.number)
    
class EpaycoLateConfirmation(models.Model):
    status_options = [(0, 'OK'), (1, 'Por resolver')] 
    
    transaction = models.OneToOneField(Transaccion, on_delete=models.CASCADE, default=None, null=True, verbose_name='Transacción')   
    status = models.IntegerField('Estado', choices=status_options, default=0)
    json_data = models.TextField('Datos Json', default='', null=True, blank=True)
    description = models.TextField('Descripción', default='', null=True, blank=True)
    
    def __str__(self):
        return 'Para ' + str(self.transaction)


                    

                 
                    