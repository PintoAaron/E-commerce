from twilio.rest import Client
from django.conf import settings



def send_otp_sms(phone_number, otp):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        client.messages.create(
            body=f"PintoShop: {otp}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        return 'sent'
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return str(e)