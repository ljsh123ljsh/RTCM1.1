import asyncio
import time
from base64 import b64encode
from binascii import b2a_hex
from random import random
from random import choice
import main_test

async def connect_cors():
    k = 1
    while k:
        connect = asyncio.open_connection(host, port)
        reader, writer = await connect
        EncryptionStr = b64encode(str.encode(user + ':' + passqord))
        header = 'GET /' + mountpoint + ' HTTP/1.1\r\nUser-Agent: NTRIP ZHDGPS\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic ' + bytes.decode(EncryptionStr) + '\r\n\r\n'
        writer.write(header.encode())
        await writer.drain()
        line = await reader.readline()
        print(line)
        k += 1
        if line == b'ICY 200 OK\r\n':
            global success_number
            success_number += 1
            print("第{}个登录成功".format(success_number))
            while 1:
                # 获取不同时间段的GGA，并转换为字节流
                a = time.strftime('%H%M%S', time.localtime(time.time()))
                a = int(a)-80000
                if a < 0:
                    a = a+120000
                B = round(3114.67923534 + random()*locaion_range*choice([1, -1]), 7)
                L = round(12135.54812367 + random()*locaion_range*choice([1, -1]), 7)
                GGA = '$GPGGA,' + str(a) + ','+str(B)+',N,'+str(L)+',E,1,24,0.6,43.580,M,-6.251,M,,*47'
                print(GGA)
                GGA = str.encode(GGA)
                # 发送GGA，方法同Socket.sendall(GGA)
                writer.write(GGA)
                await writer.drain()
                # 接收差分数据，方法同Socket.recv(1024)
                Msg = await reader.read(5000)
                Msg = b2a_hex(Msg).decode('utf-8')
                # 打印差分数据，根据需要选择是否屏蔽
                main_test.map_d30(Msg)

                print(Msg)
                await asyncio.sleep(1)
        if k > 5:
            global fail_number
            print('第{}个登录失败'.format(fail_number + 1))
            fail_number += 1
            return -1



if __name__ == '__main__':
    host = '120.204.202.101'
    port = 8691
    user = 'cmcc123'
    passqord = 'cmcc_123'
    mountpoint = 'source3'
    fail_number = 0
    success_number = 0
    locaion_range = 1  # 模拟范围
    simulator_number = 1  # 模拟数量

    #定义事件循环
    task = [connect_cors() for i in range(simulator_number)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(task))