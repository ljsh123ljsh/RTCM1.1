import _thread
import asyncio
import threading
import time

import pika
import redis
from retry import retry
import pandas as pd

from RTCM.stable.configReader import ConfigReader

class Consumer:
    @retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
    def __init__(self):

        credentials = pika.PlainCredentials('raiky', 'raiky')
        #建立连接
        connection = pika.BlockingConnection(pika.ConnectionParameters("192.168.130.17","5672","/",credentials))
        #创建channel
        channel = connection.channel()
        channel.exchange_declare(exchange='data_topic', exchange_type='topic')
        result = channel.queue_declare('',exclusive=True)
        queue_name = result.method.queue
        binding_key = 'data.msm.*'
        channel.basic_qos(prefetch_count=10)

        channel.queue_bind(exchange='action_topic', queue=queue_name, routing_key=binding_key)
        channel.basic_consume(queue_name,
                              self.callback,
                              False)
        # 不用确认消息
        print(" [*] Waiting for messages. To exit press Ctrl + C ")
        try:
            channel.start_consuming()  # 监听数据
        # Don't recover connections closed by server
        except pika.exceptions.ConnectionClosedByBroker as e:
            print("*************************************************************")
            print(e)

    #定义回调函数用于取出队列中的数据
    def callback(self,ch, method, properties, body):
        print(" [x] Received %r" % body)

        if (isinstance(body, bytes)):
            body = bytes.decode(body)
        bodyL=body.split(",")
        if(len(bodyL) == 5):
            actionKey=bodyL[0].split(".")[1]
            if actionKey in action:
                dict_action[actionKey]=dict_action[actionKey].append([{"testId":bodyL[1],"status":bodyL[3],"time":bodyL[4]}], ignore_index=True)
        ch.basic_ack(delivery_tag=method.delivery_tag)



        # ch.basic_ack(delivery_tag=method.delivery_tag)
def dealData():
    while [ 1 ]:
        for i in action:
            asyncio.run(makeDataFrame(i))
                # print(msg)
        # print(dict_action)
        print(dict_monitor)
        time.sleep(1)
async def makeDataFrame(i):
    groups = dict_action[i].groupby("testId")
    for name, group in groups:
        print(dict_start[name])
        if(dict_start[name]==None):
            dict_start[name]=0
            break
        elif(dict_start[name] < 10):
            dict_start[name]+=1
            break
        else:
            print("start monitor")
            dict_start[name] += 1
            if (not group.empty):
                dict_monitor[i]=group.shape[0]
                minTime = int(group.min().get("time"))
                if (minTime != None):
                    colNum0 = group.loc[(group["time"] == str(minTime)) & (group["status"] == "0")].shape[0]
                    colNum1 = group.loc[(group["time"] == str(int(minTime))) & (group["status"] == "1")].shape[0]
                    redis_util.redis_write(name, i, 0, {minTime: colNum0})
                    redis_util.redis_write(name, i, 1, {minTime: colNum1})
                    dict_action[i].drop(dict_action[i].loc[(dict_action[i]["time"] == str(minTime)) & (
                                dict_action[i]["testId"] == name)].index, inplace=True)
class Redis_util:
    def __init__(self):
        config = ConfigReader()
        self.r = redis.StrictRedis(host=config.getConfig("redis", "redis_addr"),
                              port=config.getConfig("redis", "redis_port"), db=config.getConfig("redis", "redis_db"))
    def redis_write(self,testId,actionkey,statusKey,msg):
        key="_".join([str(testId),actionkey,str(statusKey)])
        if(self.r.exists(key)==1):
            self.r.hsetnx(key,msg)
        else:
            self.r.hsetex(key,600,msg)

if __name__ == "__main__" :
    global action
    global dict_action
    global dict_monitor
    global dict_start
    dict_start={}
    action=["connect", "login", "send", "rec", "basefilter"]
    dict_action={}
    dict_monitor={}
    redis_util=Redis_util()
    for i in action:
        dict_action[i] = pd.DataFrame(columns=('testId','time', 'status'))
        dict_monitor[i]=0
    # t=threading.Thread(target=dealData())
    # t.start()
    _thread.start_new_thread(dealData,())
    c=Consumer()




