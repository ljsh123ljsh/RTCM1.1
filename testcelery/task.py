# coding:utf-8
from testcelery import *

import subprocess

from time import sleep

from celery import Celery

backend = 'redis://:{}@{}:{}/4'.format(redis['password'], redis['host'], redis['port'])

broker = 'redis://:{}@{}:{}/3'.format(redis['password'], redis['host'], redis['port'])

app = Celery('tasks', backend=backend, broker=broker)


@app.task
def add(x):
    sleep(1)
    print(x+5)
    return x + 5


@app.task
def hostname():
    print(subprocess.check_output(['hostname']))
    return subprocess.check_output(['hostname']).decode('utf-8')