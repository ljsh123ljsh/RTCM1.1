from configparser import ConfigParser

cf = ConfigParser()
try:
    cf.read('C:/Users/lvjia/PycharmProjects/RTCM1.1/conf.ini', encoding='ANSI')
except:
    cf.read('../conf.ini')

rabbitmq = {
    'host': cf.get('rabbitmq', 'host'),
    'port': cf.get('rabbitmq', 'port'),
    'user': cf.get('rabbitmq', 'user'),
    'password': cf.get('rabbitmq', 'password'),
    'exchange': cf.get('rabbitmq', 'exchange')
}

mysql = {
    'host': cf.get('mysql', 'host'),
    'port': cf.get('mysql', 'port'),
    'user': cf.get('mysql', 'user'),
    'password': cf.get('mysql', 'password'),
    'db': cf.get('mysql', 'db')
}
redis = {
    'host': cf.get('redis', 'host'),
    'port': cf.get('redis', 'port'),
    'password': cf.get('redis', 'password'),
    'db': cf.get('redis', 'db')
}
