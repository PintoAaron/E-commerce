from .models import Customer
from kafka import KafkaProducer
from dotenv import load_dotenv
import os


load_dotenv()

kafka_topic = "pintoshop_orders"
server = os.getenv('KAFKA_SERVER')

def send_order_to_kafka(customer_id):
    customer = Customer.objects.select_related('user').get(pk = customer_id)
    producer = KafkaProducer(bootstrap_servers=server)
    
    print("sending data to kafka_topic....")
    
    data = ",".join([customer.user.first_name,customer.user.last_name,customer.user.email])
    
    producer.send(topic=kafka_topic, value=data.encode('utf-8'))
    
    print("message successfully sent to kafka_topic")
        
    producer.flush()

    producer.close()