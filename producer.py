import pika
import json
import random
from contact_model import Contact
from mongoengine import connect

# Підключення до бази даних MongoDB
connect('Cluster0', host='mongodb+srv://ms_miracle18:ryPanrIWBPIoqX0T@cluster0.d6hdlvu.mongodb.net/')

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення черги
channel.queue_declare(queue='email_queue')

# Генерація фейкових контактів та відправка їх в чергу RabbitMQ
for _ in range(10):  # Згенеруємо 10 контактів для прикладу
    full_name = f'User{random.randint(1, 100)}'
    email = f'user{random.randint(1, 100)}@example.com'
    
    # Збереження контакту в базі даних
    contact = Contact(full_name=full_name, email=email)
    contact.save()
    
    # Поміщення ID контакту у чергу
    message = {
        'contact_id': str(contact.id)
    }
    channel.basic_publish(exchange='', routing_key='email_queue', body=json.dumps(message))

print("Повідомлення про контакти надіслано у чергу RabbitMQ")
connection.close()
