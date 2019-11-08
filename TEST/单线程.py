#!/usr/bin/env
# coding:utf8
# Author: hz_oracle

import pymysql
import requests
import time


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
        urls_list = list()
        try:
            self.cursor.execute(sql)
            fetchresult = self.cursor.fetchall()
            for line in fetchresult:
                urls_list.append(line[0])
            print (len(urls_list))
        except Exception as e:
            print (u"数据库查询失败:%s"  % e)
            return []
        return urls_list

    def db_close(self):
        self.conn.close()


def get_pic(url):
    try:
        pic_obj = requests.get(url).content
    except Exception as e:
        print (u"图片出错")
        return ""
    filename = url.split('/')[-2]
    file_path = "./picture/" + filename + '.jpg'
    fp = open(file_path, 'wb')
    fp.write(pic_obj)
    fp.close()
    return "ok"


def main():
    start_time = time.time()
    db_obj = DbHandler(host='192.168.238.133', port=3306, user='root', pwd='123456', dbname='test')
    db_obj.db_conn()
    url_list = db_obj.get_urls(100)
    map(get_pic, url_list)
    #for url in url_list:
    #    get_pic(url)
    end_time = time.time()
    costtime = float(end_time) - float(start_time)
    print (costtime)
    print ("download END")

if __name__ == "__main__":
    main()
