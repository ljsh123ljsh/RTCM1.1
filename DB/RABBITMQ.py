import pika
from DB import rabbitmq

RABBITMQ = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq['host'], port=int(rabbitmq['port']), credentials=pika.PlainCredentials(password=rabbitmq['password'], username=rabbitmq['user']))).channel()
exchange = rabbitmq['exchange']