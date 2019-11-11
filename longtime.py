import time
import asyncio
from base64 import b64encode
from binascii import b2a_hex
from random import random
from random import choice
from stable.Tool import map_d30
from RTCM_ANALYSE import Analyse
import socket
import load2redis
'''
模拟 + 解析
'''

def connect_cors():
    k = 1
    while k:
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))
        EncryptionStr = b64encode(str.encode(user + ':' + passqord))
        header = 'GET /' + mountpoint + ' HTTP/1.1\r\nUser-Agent: NTRIP ZHDGPS\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic ' + bytes.decode(EncryptionStr) + '\r\n\r\n'
        conn.sendall(header.encode())
        line = conn.recv(4096)
        print(line)
        k += 1
        if line == b'ICY 200 OK\r\n\r\n':
            global success_number
            success_number += 1
            print("第{}个登录成功".format(success_number))
            while 1:
                # 获取不同时间段的GGA，并转换为字节流
                a = time.strftime('%H%M%S', time.localtime(time.time()))
                a = int(a)-80000
                if a < 0:
                    a = a+120000
                # 随机位置
                B = round(3114.67923534 + random()*locaion_range*choice([1, -1]), 7)
                L = round(12135.54812367 + random()*locaion_range*choice([1, -1]), 7)
                GGA = '$GPGGA,' + str(a) + ','+str(B)+',N,'+str(L)+',E,1,24,0.6,43.580,M,-6.251,M,,*47'
                print(GGA)
                GGA = str.encode(GGA)
                # 发送GGA，方法同Socket.sendall(GGA)
                conn.sendall(GGA)
                # 接收差分数据
                Msg = conn.recv(1500)
                Msg = b2a_hex(Msg).decode('utf-8')
                # 打印差分数据，根据需要选择是否屏蔽

                # 解算差分
                gen = map_d30(Msg)
                while 1:
                    try:
                        data = next(gen)
                    except StopIteration:
                        print("——" * 30)
                        print('COMPLETE')
                        print("——"*50)
                        break
                    try:
                         Analyse.analyse(data)
                    except KeyError:
                         load2redis.main()

                    except:
                        continue
                # 解算完成

                print(Msg)
                time.sleep(1)
        if k > 5:
            global fail_number
            print('第{}个登录失败'.format(fail_number + 1))
            fail_number += 1
            return -1


if __name__ == '__main__':
    host = '192.168.130.54'
    port = 8201
    user = 'cmcc123'
    passqord = 'cmcc_123'
    mountpoint = 'source6'
    fail_number = 0
    success_number = 0
    locaion_range = 1  # 模拟范围
    simulator_number = 1  # 模拟数量
    connect_cors()