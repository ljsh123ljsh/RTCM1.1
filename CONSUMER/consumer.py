from CONSUMER import *

class Consumer:

    def __init__(self):

        channel = RABBITMQ.RABBITMQ
        channel.exchange_declare(exchange='my1', exchange_type='topic')
        result = channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        binding_key = 'data.msm'
        channel.basic_qos(prefetch_count=10)

        channel.queue_bind(exchange='my1', queue=queue_name, routing_key=binding_key)
        channel.basic_consume(queue_name, self.callback, False)
        # 不用确认消息
        print(" [*] Waiting for messages. ")
        try:
            channel.start_consuming()  # 监听数据
        except pika.exceptions.ConnectionClosedByBroker as e:
            print("*************************************************************")
            print(e)

    #定义回调函数用于取出队列中的数据
    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)

        if isinstance(body, bytes):
            body = bytes.decode(body)
        bodyL = body.split(",")
        if len(bodyL) == 5:
            actionKey = bodyL[0].split(".")[1]
            if actionKey in action:
                dict_action[actionKey] = dict_action[actionKey].append([{"testId": bodyL[1], "status":bodyL[3], "time": bodyL[4]}], ignore_index=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == "__main__" :
    dict_start={}
    action = ["connect", "login", "send", "rec", "basefilter"]
    dict_action = {}
    dict_monitor = {}
    c = Consumer()

