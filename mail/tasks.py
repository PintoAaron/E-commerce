from django.core.mail import EmailMessage,BadHeaderError
from templated_mail.mail import BaseEmailMessage
from shop.models import Customer
from celery import shared_task


@shared_task
def order_created_task(order):
    customer = Customer.objects.select_related('user').get(pk = order.customer_id)
    print("SENDING MAIL TO CUSTOMER ABOUT ORDER")
    try:
        message = EmailMessage(
            'Order Received',
            f'Hello {customer.user.first_name}, we have successfully received your order and it is undergoing processing.',
            'aaronpinto111@gmail.com',
            [customer.user.email]
        )
        message.attach_file('media/Pintoshop.png')
        message.send()
        print("MAIL ABOUT ORDER SUCCESSFULLY SENT")
    except BadHeaderError:
        print("MAIL ABOUT ORDER NOT SENT")
        pass


@shared_task
def new_user_task(user):
    print("SENDING MAIL TO NEW USER")
    try:
        message = BaseEmailMessage(
            template_name='emails/welcome.html'
            )
        message.send([user])
        print("MAIL SUCCESSFULLY SENT")
    except BadHeaderError:
        pass
    print("MAIL NOT SENT")