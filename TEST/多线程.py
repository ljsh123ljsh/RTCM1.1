#!/usr/bin/env python
# coding:utf8
# Author: hz_oracle

import pymysql
import requests
import time
import threading
# import Queue

lock1 = threading.RLock()
url_queue = Queue.Queue()
urls_list = list()


class DbHandler(object):
    def __init__(self, host, port, user, pwd, dbname):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = dbname

    def db_conn(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.pwd, db=self.db, charset="utf8")
            self.cursor = self.conn.cursor()
            return 1
        except Exception as e:
            return 0

    def get_urls(self, limitation):
        sql = """select pic  from  picurltable limit  %s""" % limitation
        try:
            self.cursor.execute(sql)
            fetchresult = self.cursor.fetchall()
            for line in fetchresult:
                url_queue.put(line[0])
        except Exception as e:
            print(u"数据库查询失败:%s"  % e)
            return 0
        return 1

    def db_close(self):
        self.conn.close()


class MyThread(threading.Thread):
    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):
        url = url_queue.get()
        try:
            pic_obj = requests.get(url).content
        except Exception as e:
            print(u"图片出错")
            return ""
        filename = url.split('/')[-2]
        file_path = "./picture/" + filename + '.jpg'
        fp = open(file_path, 'wb')
        fp.write(pic_obj)
        fp.close()


def main():
    start_time = time.time()
    db_obj = DbHandler(host='127.0.0.1', port=3306, user='root', pwd='123456', dbname='pic')
    db_obj.db_conn()
    db_obj.get_urls(100)
    for i in range(100):
        i = MyThread()
        i.start()
    while True:
        if threading.active_count()<=1:
            break
    end_time = time.time()
    costtime = float(end_time) - float(start_time)
    print(costtime)
    print( "download END")

if __name__ == "__main__":
    main()
