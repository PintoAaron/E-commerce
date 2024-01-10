from shop.signals import order_created_signal
from django.dispatch import receiver
from shop.models import Customer


@receiver(order_created_signal)
def send_mail(sender,**kwargs):
    if kwargs['order']:
        order = kwargs['order']
        customer = Customer.objects.select_related('user').get(pk = order.customer_id)
        #print(f"Hello {customer.user.first_name}, we have received your order and its under going processing")
        
        