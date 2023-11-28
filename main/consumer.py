import pika, json#, os, django

from main import Product, db, app

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
#django.setup()

#app = create_app()

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='rabbitmq',
    connection_attempts=10,
    retry_delay=10,
    heartbeat=0,
))
channel = connection.channel()
# channel.queue_declare(queue='main')

channel.exchange_declare(exchange='ex_main', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange='ex_main', queue=queue_name)

def callback(ch, method, properties, body):
    print("********************************** properties.content_type", properties.content_type)
    with app.app_context():
        print('Received in admin',  body)
        data = json.loads(body)
        print("data :", data)
        
        if properties.content_type == 'product_created':
            product = Product(id=data['id'], title=data['title'], image=data['image'])
            db.session.add(product)
            db.session.commit()
            print('Product Created')

        elif properties.content_type == 'product_updated':
            product = Product.query.get(data['id'])
            product.title = data['title']
            product.image = data['image']
            print(f"{product}, {product.title}, {product.image}, is going to update")
            db.session.commit()
            print('Product Updated')

        elif properties.content_type == 'product_deleted':
            product = Product.query.get(data)
            db.session.delete(product)
            db.session.commit()
            print('Product Deleted')

        # id = json.loads(body)
        # print(id)
        # product = Product.objects.get(id=id)
        # product.likes = product.likes + 1
        # product.save()
        #print('Product likes increased!')


# channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)


try:
    print('Started Consuming')
    channel.start_consuming()
except pika.exceptions.ConnectionClosedByBroker as e:
    print(f"Connection closed by broker: {e}")
finally:
    channel.close()
