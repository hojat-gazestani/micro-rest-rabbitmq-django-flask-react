import pika, json

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='rabbitmq',
    connection_attempts=5,
    retry_delay=5,
    heartbeat=0,
))

channel = connection.channel()

channel.queue_declare(queue='main')


def publish(method='method', body='body'):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
    print(" [x] Sent 'New message'")

# publish()
#connection.close()

