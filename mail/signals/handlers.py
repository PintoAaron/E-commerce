from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from shop.signals import order_created_signal
from ..tasks import order_created_task,new_user_task


@receiver(order_created_signal)
def send_order_received_mail(sender,**kwargs):
    if kwargs['order']:
        order = kwargs['order']
        customer = order.customer_id
        order_created_task.delay(customer)
        
        

@receiver(post_save,sender=settings.AUTH_USER_MODEL)    
def send_welcome_message_to_new_user(sender,**kwargs):
    if kwargs['created']:
        new_user = kwargs['instance']
        new_user_task.delay(new_user.email,new_user.first_name)
    

  