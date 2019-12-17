# coding=utf-8

import logging
import time
from queue import Queue

import pika


class MQBase(object):
    """ 消息队列基类, 该类线程不安全的 """

    def __init__(self, host, port, exchange, exchange_type='direct', ack=True, persist=True,
                 **kwargs):  # 默认开启手动消息确认, 交换机\队列\消息持久化
        """ 当开启手动消息确认, 要考虑消息重入的情况 """

        self._conn = None
        self._channel = None
        self._properties = None

        self.host = host
        self.port = port
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.ack = ack
        self.persist = persist

    def _get_channel(self):
        """ 创建连接与信道, 声明交换机 """

        if self._check_alive():
            return
        else:
            self._clear()

        if not self._conn:
            self._conn = pika.BlockingConnection(pika.ConnectionParameters(host=self.host,
                                                                           port=self.port,
                                                                           heartbeat=0))  # 建立连接并关闭心跳检测
        if not self._channel:
            self._channel = self._conn.channel()  # 建立信道
            self._channel.exchange_declare(exchange=self.exchange,
                                           exchange_type=self.exchange_type,
                                           durable=self.persist)  # 声明交换机
            if self.ack:
                self._channel.confirm_delivery()  # 在该信道中开启消息确认
            self._properties = pika.BasicProperties(delivery_mode=(2 if self.persist else 0))  # 消息持久化

    def _clear(self):
        """ 清理连接与信道 """

        def clear_conn():
            if self._conn and self._conn.is_open:
                self._conn.close()
            self._conn = None

        def clear_channel():
            if self._channel and self._channel.is_open:
                self._channel.close()
            self._channel = None

        if not (self._conn and self._conn.is_open):
            clear_conn()  # 清理连接
        clear_channel()  # 清理信道

    def _check_alive(self):
        """ 检查连接与信道是否存活 """

        return self._channel and self._channel.is_open and self._conn and self._conn.is_open


class MQSender(MQBase):
    """ 生产者, 该类是线程不安全的 """

    def send(self, route, msg):
        def try_send():
            try:
                self._get_channel()
                success = self._channel.basic_publish(exchange=self.exchange,
                                                      routing_key=route,
                                                      body=msg,
                                                      properties=self._properties)
            except Exception as e:
                success = False

            return success

        ret = try_send() or try_send()
        if not ret:
            self._clear()

        return ret


class MQReceiver(MQBase):
    """
    消费者, 该类是线程安全的
    通过receive_queue支持多线程, 不直接创建多实例是想减少底层TCP连接
    """

    def __init__(self, *args, **kwargs):
        self._has_start = False
        self.prefetch_count = kwargs.get('prefetch_count', 1)  # 每次只接受prefetch_count条消息, 处理完再接收新的
        self.receive_queue = Queue(self.prefetch_count)  # 接收缓冲队列, 线程安全的
        super(self.__class__, self).__init__(*args, **kwargs)

    def _declare_queue(self, queue_name):
        """ 声明队列 """

        self._channel.queue_declare(queue=queue_name, durable=self.persist)  # 声明队列
        self._channel.queue_bind(queue=queue_name, exchange=self.exchange, routing_key=queue_name)  # 绑定队列到交换机

    def _subscribe_queue(self, queue_route):
        """ 订阅队列  """

        try:
            self._declare_queue(queue_route)
            self._channel.basic_qos(prefetch_count=self.prefetch_count)  # 负载均衡
            self._channel.basic_consume(self._handler, queue_route, no_ack=not self.ack)  # 订阅队列, 并分配消息处理器

        except Exception as e:
            return False

        return True

    def _handler(self, channel, method_frame, header_frame, body):  # 消息处理器
        """ 收到消息后的回调 """

        print('wait message num is {num}'.format(num=channel.get_waiting_message_count()))
        self.receive_queue.put((body, self._conn, channel, method_frame.delivery_tag))  # 压入队列

    def start(self, queue_route):
        """ 开始消费 """

        if self._has_start:
            return
        try:
            self._get_channel()
            if self._subscribe_queue(queue_route):
                self._channel.start_consuming()  # 开始消费, 一个连接下仅能调用该方法一次, 否则抛出RecursionError

        except Exception as e:
            pass

    def _clear(self):

        self.receive_queue = Queue(self.prefetch_count)  # 避免消息重入缓冲队列
        super(self.__class__, self)._clear()


def main():
    from threading import Thread, current_thread
    from functools import partial

    def producer_func():
        for index in range(50):
            print('sender send {content}'.format(content=index))
            sender.send('test_queue', index)

    def consumer_func():
        receiver.start('test_queue')

    def deal_message(r):
        while True:
            msg, conn, channel, ack_tag = r.receive_queue.get()
            interval = int(msg) / 5.0
            print('{thread_name}: get {msg}, wait {interval}s, ack_tag is {delivery_tag}'.format(
                msg=msg, thread_name=current_thread().getName(), interval=interval, delivery_tag=ack_tag))
            if current_thread().getName() == 'handler_1':  # 测试负载均衡
                time.sleep(60)
            else:
                time.sleep(interval)
            conn.add_callback_threadsafe(partial(channel.basic_ack, ack_tag))  # 确认消息成功处理

    handler_num = 5
    sender = MQSender(host='localhost', port=5680, exchange='test_exchange')
    receiver = MQReceiver(host='localhost', port=5680, exchange='test_exchange', prefetch_count=handler_num)

    Thread(target=consumer_func).start()  # 消费者
    Thread(target=producer_func).start()  # 生产者

    for i in range(handler_num):
        Thread(target=deal_message, args=(receiver,), name='handler_%d' % i).start()  # 消息处理器


if __name__ == '__main__':
    main()