import pika, json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RMQProducer:
    def __init__(self, host='rabbitmq'):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=host,
                    connection_attempts=10,
                    retry_delay=10,
                    heartbeat=0,
                )
            )
            self.channel = self.connection.channel()
            # self.channel.queue_declare(queue='main')
            self.channel.exchange_declare(exchange='ex_admin', exchange_type='fanout')
        except Exception as e:
            logger.error(f"Error establishing RabbitMQ connection: {str(e)}")
            raise

    def publish(self, method, body):
        try:
            properties = pika.BasicProperties(method)
            # channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
            self.channel.basic_publish(exchange='ex_admin', routing_key='', body=json.dumps(body), properties=properties)
            logger.info(f"{json.dumps(body)} Published")
        except Exception as e:
            logger.error(f"Error publishing message: {str(e)}")
            # You might want to handle this error according to your application's needs
            raise

    def close_connection(self):
        try:
            self.connection.close()
        except Exception as e:
            logger.error(f"Error closing RabbitMQ connection: {str(e)}")
            raise


if __name__ == '__main__':
    producer = None
    try:
        producer = RMQProducer()
        # producer.publish('your_method', {'key': 'value'})
        # how to pass this created producer to view and use it
    finally:
        if producer:
            producer.close_connection()

