import pika, os
from dotenv import load_dotenv
load_dotenv()

def send(queue,body):
    # Access the CLODUAMQP_URL environment variable and parse it (fallback to localhost)
    try:
        url = os.environ.get(os.getenv("RABBITMQ_URL"),
                             'RABBITMQ_AMQPS')
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()  # start a channel
        channel.queue_declare(queue=queue)  # Declare a queue
        channel.basic_publish(exchange='',
                              routing_key=queue,
                              body=body)
        connection.close()
        return True
    except Exception:
        return Exception

def receive():
    url = os.environ.get(os.getenv("RABBITMQ_URL"),
                         'RABBITMQ_AMQPS')
    params = pika.URLParameters(url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()  # start a channel
    channel.queue_declare(queue='hello')  # Declare a queue

    def callback(ch, method, properties, body):
        print(body)

    channel.basic_consume('hello',
                          callback,
                          auto_ack=True)

    print(' [*] Waiting for messages:')
    channel.start_consuming()
    connection.close()

