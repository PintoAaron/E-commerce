from django.core.mail import EmailMessage,BadHeaderError
from shop.models import Customer
from celery import shared_task


@shared_task
def order_created_task(customer_id):
    customer = Customer.objects.select_related('user').get(pk = customer_id)
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


@shared_task
def new_user_task(user_email,username):
    try:
        message = EmailMessage(
            'PintoShop Account',
            f'Hello {username}, you have successfully created an account with pintoshop, go ahead ad start shopping',
            'aaronpinto111@gmail.com',
            [user_email]
        )
        message.send()
    except BadHeaderError:
        pass