from myCeleryProj import *
from myCeleryProj.app import app


@app.task
def task1(content):
    content_lis = segment_d30(content)
    thread_list = []
    for data in content_lis:
        thr = Thread(target=analyse, args=(data, ))
        thread_list.append(thr)
    for l in thread_list:
        l.start()

@app.task
def task2(content):
    content_lis = segment_d30(content)
    thread_list = []
    for data in content_lis:
        thr = Thread(target=analyse, args=(data, ))
        thread_list.append(thr)
    for l in thread_list:
        l.start()


