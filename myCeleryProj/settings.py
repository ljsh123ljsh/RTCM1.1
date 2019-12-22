from kombu import Queue
from myCeleryProj import *
  
# CELERY_QUEUES = (  # 定义任务队列
#     Queue("default", routing_key="task.#"),  # 路由键以“task.”开头的消息都进default队列
#     Queue("tasks_A", routing_key="A.#"),  # 路由键以“A.”开头的消息都进tasks_A队列
#     Queue("tasks_B", routing_key="B.#"),  # 路由键以“B.”开头的消息都进tasks_B队列
# )
# 设置详细的队列
CELERY_QUEUES = {
    "default": {  # 这是上面指定的默认队列
        "exchange": "data_topic",
        "exchange_type": "direct",
        "routing_key": "default"
    },
    "test": {  # 这是一个topic队列 凡是topictest开头的routing key都会被放到这个队列
        "routing_key": "data.msm",
        "exchange": "data_topic",
        "exchange_type": "topic",
    },
    "task_eeg": {  # 设置扇形交换机
        "exchange": "data_topic",
        "exchange_type": "fanout",
        "binding_key": "tasks",
    },
}

CELERY_ROUTES = (
     [
         ("myCeleryProj.tasks.task1", {"queue": "default"}),# 将taskA任务分配至队列 tasks_A
         ("myCeleryProj.tasks.task2", {"queue": "default"}),# 将taskB任务分配至队列 tasks_B
     ],
 )
BROKER_URL = 'amqp://{}:{}@{}:{}//'.format(rabbitmq['user'], rabbitmq['password'], rabbitmq['host'], rabbitmq['port'])
# print(BROKER_URL)
# BROKER_URL = "amqp://raiky:raiky@192.168.30.88:5672//"  # 使用mq 作为消息代理
# BROKER_URL = "amqp://raiky:raiky@192.168.30.88:5672//"
CELERY_RESULT_BACKEND = 'redis://:{}@{}:{}/3'.format(redis['password'], redis['host'], redis['port'])
# print(CELERY_RESULT_BACKEND)
# CELERY_RESULT_BACKEND = "redis://:123456@192.168.30.88:6379/0"  # 任务结果存在Redis
 
CELERY_RESULT_SERIALIZER = "json"  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
CELERY_DEFAULT_QUEUE = 'test'
 
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显


CELERY_TASK_SERIALIZER = 'msgpack'
# 指定结果序列化方式
# CELERY_RESULT_SERIALIZER = 'msgpack'
# 任务过期时间,celery任务执行结果的超时时间
# CELERY_TASK_RESULT_EXPIRES = 60 * 20
# 指定任务接受的序列化类型.
CELERY_ACCEPT_CONTENT = ["msgpack"]
# 任务发送完成是否需要确认，这一项对性能有一点影响
CELERY_ACKS_LATE = True
# 压缩方案选择，可以是zlib, bzip2，默认是发送没有压缩的数据
CELERY_MESSAGE_COMPRESSION = 'zlib'
# 规定完成任务的时间
CELERYD_TASK_TIME_LIMIT = 5  # 在5s内完成任务，否则执行该任务的worker将被杀死，任务移交给父进程
# celery worker的并发数，默认是服务器的内核数目,也是命令行-c参数指定的数目
CELERYD_CONCURRENCY = 4
# celery worker 每次去rabbitmq预取任务的数量
CELERYD_PREFETCH_MULTIPLIER = 4
# 每个worker执行了多少任务就会死掉，默认是无限的
CELERYD_MAX_TASKS_PER_CHILD = 40
# 设置默认的队列名称，如果一个消息不符合其他的队列就会放在默认队列里面，如果什么都不设置的话，数据都会发送到默认的队列中
# CELERY_DEFAULT_QUEUE = "default"
