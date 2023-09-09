import pika
import json
import time
from contact_model import Contact
from mongoengine import connect

# Підключення до бази даних MongoDB
connect('my_database', host='mongodb://localhost:27017/')

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Створення черги
channel.queue_declare(queue='email_queue')

def send_email(contact_id):
    # Функція для імітації надсилання email
    print(f"Відправлено email для контакту з ID {contact_id}")
    time.sleep(2)  # Імітуємо відправку email
    contact = Contact.objects.get(id=contact_id)
    contact.message_sent = True
    contact.save()

def callback(ch, method, properties, body):
    # Обробка повідомлення з черги
    message = json.loads(body)
    contact_id = message['contact_id']
    send_email(contact_id)
    print(f"Повідомлення для контакту з ID {contact_id} оброблено")

# Підписка на чергу та очікування повідомлень
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print("Чекаємо на повідомлення...")
channel.start_consuming()
