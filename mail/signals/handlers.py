from django.core.mail import EmailMessage,BadHeaderError
from django.db.models.signals import post_save
from django.conf import settings
from shop.signals import order_created_signal
from django.dispatch import receiver
from shop.models import Customer


@receiver(order_created_signal)
def send_order_received_mail(sender,**kwargs):
    if kwargs['order']:
        order = kwargs['order']
        customer = Customer.objects.select_related('user').get(pk = order.customer_id)
        try:
            message = EmailMessage(
                'Order Received',
                f'Hello {customer.user.first_name}, we have successfully received your order and it is undergoing processing.',
                'aaronpinto111@gmail.com',
                [customer.user.email]
            )
            message.attach_file('media/Pintoshop.png')
            message.send()
        except BadHeaderError:
            pass
        

@receiver(post_save,sender=settings.AUTH_USER_MODEL)    
def send_welcome_message_to_new_user(sender,**kwargs):
    if kwargs['created']:
        to_email = kwargs['instance']
        try:
            message = EmailMessage(
                'Welcome To PintoShop',
                '''
                Hi, 
                You have successfullly created an account with PintoShop
                Go ahead and start shopping
                ''',
                'aaronpinto111@gmail.com',
                [to_email]
                
            )
            message.send()
        except BadHeaderError:
            pass
    

  