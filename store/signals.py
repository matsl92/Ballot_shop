from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Rifa, Balota

@receiver(post_save, sender=Rifa, dispatch_uid="create_ballots")
def create_ballots(sender, instance, created, **kwargs):
    """
    The dispatch_uid parametter is recomended in some cases, for instance, 
    when the receiver sends emails, because it prevents multiple signal-receiver 
    registrations, which may happend if not set.
    """
    n = (instance.max_number+1 - instance.min_number) // instance.step   
    if instance.min_number <= instance.max_number and n > 0:
        for i in range((instance.max_number+1-instance.min_number)//instance.step):
            if not instance.min_number + instance.step*i in [
                ballot.number for ballot in Balota.objects.filter(lottery=instance)
            ]:  
                ballot = Balota(
                    number=instance.min_number+instance.step*i, 
                    price = instance.ballot_price, 
                    unavailable_time = instance.ballot_unavailable_time, 
                    lottery = instance
                )
                ballot.save()

@receiver(post_save, sender=Rifa, dispatch_uid="handle_is_active_attribute")
def handle_is_active_attribute(sender, instance, created, **kwargs):             
    if instance.is_active:
            for lottery in instance.society.rifa_set.all():
                if lottery != instance and lottery.is_active:
                    lottery.is_active = False
                    lottery.save()  
                    print('lottery set to not active')          

   