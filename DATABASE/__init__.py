from redis import StrictRedis
from pymysql import connect
import pika

REDIS = StrictRedis(host='192.168.130.86', port=6379, db=10, password='123456')
MYSQL = connect(host='192.168.130.86', port=8306, user='root', password='cmcc_123456', db='singal')
RABBITMQ = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.130.86', port=5672, credentials=pika.PlainCredentials(password='cmccsy', username='cmccsy'))).channel()