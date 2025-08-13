from django.conf import settings
import redis

REDIS_URL = settings.CELERY_BROKER_URL
redis_client = redis.StrictRedis.from_url(REDIS_URL, decode_responses=True)

class OTPManager:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def store_otp(self, phone_number, otp, expiry=600):
        key = f"otp:{phone_number}"
        self.redis_client.setex(key, expiry, otp)
        return True

    def get_otp(self, phone_number):
        key = f"otp:{phone_number}"
        return self.redis_client.get(key)

    def delete_otp(self, phone_number):
        key = f"otp:{phone_number}"
        self.redis_client.delete(key)
        return True

otp_manager = OTPManager(redis_client)