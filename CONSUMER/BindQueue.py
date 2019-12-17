from CONSUMER import *

def callback(ch, method, properties, body):
    body = bytes.decode(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(body)
    return body

channel = RABBITMQ.RABBITMQ
channel.exchange_declare(exchange=RABBITMQ.exchange, exchange_type='topic')
result = channel.queue_declare(queue=RABBITMQ.queue, exclusive=True)
queue_name = result.method.queue

binding_key = 'data.msm'
channel.queue_bind(exchange=RABBITMQ.exchange, queue=queue_name, routing_key=binding_key)
channel.basic_consume(queue_name, callback, False)
channel.start_consuming()