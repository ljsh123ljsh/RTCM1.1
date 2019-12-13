from CONSUMER import *

def callback(ch, method, properties, body):
        # print(" [x] Received %r" % body)
        if isinstance(body, bytes):
            body = bytes.decode(body)
            yield body
        bodyL = body.split(",")
        if len(bodyL) == 5:
            actionKey = bodyL[0].split(".")[1]
            if actionKey in ["connect", "login", "send", "rec", "basefilter"]:
                pass
                # dict_action[actionKey] = dict_action[actionKey].append([{"testId": bodyL[1], "status":bodyL[3], "time": bodyL[4]}], ignore_index=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)


def consume(a, b):
    channel = RABBITMQ.RABBITMQ
    channel.exchange_declare(exchange=RABBITMQ.exchange, exchange_type='topic')
    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue
    binding_key = 'data.msm'
    channel.basic_qos(prefetch_count=10)

    channel.queue_bind(exchange=RABBITMQ.exchange, queue=queue_name, routing_key=binding_key)
    channel.basic_consume(queue_name, callback, False)
    # 不用确认消息
    print(" [*] Waiting for messages. ")
    channel.start_consuming()  # 监听数据


def anal(content):
    data = Tool.map_d30(content)
    Analyse.analyse(data)


if __name__ == '__main__':
    content = consume(1, 2)
    print(content)
    # anal(content)
    # li = []
    # for i in range(1):
    #     thre = threading.Thread(target=consume, args=(1, 2))
    #     li.append(thre)
    # for l in li:
    #     l.start()

