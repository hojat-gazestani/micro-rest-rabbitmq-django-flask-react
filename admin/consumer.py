import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

# from products.models import Product

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='rabbitmq',
    connection_attempts=5,
    retry_delay=5,
    heartbeat=0,
))
channel = connection.channel()
channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in admin', body)
    # id = json.loads(body)
    # print(id)
    # product = Product.objects.get(id=id)
    # product.likes = product.likes + 1
    # product.save()
    print('Product likes increased!')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()