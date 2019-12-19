from CONSUMER import *
from RTCM_ANALYSE.Analyse import analyse
from stable.Tool import segment_d30
from threading import Thread

def analyseANDprint(content):
    content_lis = segment_d30(content)
    thread_list = []
    for data in content_lis:
        thr = Thread(target=analyse, args=(data, ))
        thread_list.append(thr)
    for l in thread_list:
        l.start()

def callback(ch, method, properties, body):
    body = bytes.decode(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    analyseANDprint(body)
    # print(body)
    return body


def consume(a, b):
    channel = RABBITMQ.RABBITMQ
    channel.exchange_declare(exchange=RABBITMQ.exchange, exchange_type='topic')
    result = channel.queue_declare(RABBITMQ.queue, exclusive=True)
    queue_name = result.method.queue
    binding_key = 'data.msm'
    channel.basic_qos(prefetch_count=10)

    channel.queue_bind(exchange=RABBITMQ.exchange, queue=RABBITMQ.queue, routing_key=binding_key)
    channel.basic_consume(queue_name, callback, False)
    # 不用确认消息
    print(" [*] Waiting for messages. ")
    channel.start_consuming()  # 监听数据




if __name__ == '__main__':
    content = consume(1, 2)
    print(content)


