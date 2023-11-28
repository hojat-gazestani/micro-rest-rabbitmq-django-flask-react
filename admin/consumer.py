import pika, json, os, django
# from asgiref import process

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
# process.setup()
from products.models import Product


connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='rabbitmq',
    connection_attempts=10,
    retry_delay=10,
    heartbeat=0,
))
channel = connection.channel()
# channel.queue_declare(queue='main')

channel.exchange_declare(exchange='ex_admin', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='ex_admin', queue=queue_name)


def callback(ch, method, properties, body):
    print('Received in admin_queue consumer', body)
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased!')


# channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)



try:
    print('Started Consuming')
    channel.start_consuming()
except pika.exceptions.ConnectionClosedByBroker as e:
    print(f"Connection closed by broker: {e}")
finally:
    channel.close()
