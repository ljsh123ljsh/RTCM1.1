 # -*- encoding:utf-8 -*-
__author__ = 'lixiaohui'

"""
脚本说明�?
ClientAsyncio_V1.0.0.py: 模拟不同并发量下的用户登录usercaster服务

变量说明�?
服务器连接变量：connect，修改服务连接IP和端�?
登录用户名变量：user （输入正确用户）
登录密码变量：pwd （输入正确密码）
登录命令变量：header，其中的source源节点、用户名及密码为变化点，脚本中源节点固定为source3
并发用户变量：concurrencyNum
"""

import asyncio,time,base64,random
import traceback
import logging

logging.basicConfig(filename='log.log')

concurrencyNum = 100

# 定义协程函数，标志为async，await需要asyncio一起使�?
async def clientGL(x):
    while 1:
        try:
            # 与服务器建立连接
            # connect = asyncio.open_connection('192.168.200.211', 6106)
            connect = asyncio.open_connection('127.0.0.1', 8088)
            reader,writer = await connect
            # 登录命令，source3为源节点（正确），zhdgps:zhdgps为用户名密码，base64编码后为emhkZ3BzOnpoZGdwcw==
            # 正确用户名密码：admin:zhdgps为用户名密码，base64编码后为YWRtaW46emhkZ3Bz
            user = 'cmcc123'
            pwd = 'cmcc_123'
            EncryptionStr = base64.b64encode(str.encode(user + pwd))
            # print(EncryptionStr)
            header = 'GET /source4 HTTP/1.1\r\nUser-Agent: NTRIP ZHDGPS\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic ' + bytes.decode(
                EncryptionStr) + '\r\n\r\n'
            # print(header)
            # 发送登录命令，write同socket.send()
            writer.write(header.encode('utf-8'))
            await writer.drain()
            # 接收服务器返回的登录信息
            line = await reader.readline()
            if line == b'\r\n':
                break
            result = line.decode('utf-8').rstrip()
            print(result)
            # 返回信息�?ICY 200 OK 时，发送GGA数据
            if result == 'ICY 200 OK':
                a = time.strftime('%H%M%S.%S', time.localtime(time.time()))
                B = 3103.14747523
                L = 12121.33538519
                GGA = '$GPGGA,' + a + ',' + str(B) + ',N,' + str(L) + ',E,1,24,0.6,43.580,M,-6.251,M,,*47'
                # print(GGA)
                GGA = str.encode(GGA)
                writer.write(GGA)
                await writer.drain()
                #while 1:
                    # 获取不同时间段的GGA，并转换为字节流
                    #a = time.strftime('%H%M%S.%S', time.localtime(time.time()))
                    #B = random.randrange(-100, 100, 1)/100*0.00833 + B
                    #L = random.randrange(-100, 100, 1)/100*0.00833 + L
                    #GGA = '$GPGGA,' + a + ',' + str(B) +',N,' + str(L) +',E,1,24,0.6,43.580,M,-6.251,M,,*47'
                    #print(GGA)
                    #GGA = str.encode(GGA)
                    #writer.write(GGA)
                    #await writer.drain()
                await reader.read(1024)
                await asyncio.sleep(1)
            else:
                print("Error")
                writer.close()
                continue
        except:
            s = traceback.format_exc()
            logging.error(s)
            writer.close()
    writer.close()

# 创建一个默认的事件循环
loop = asyncio.get_event_loop()
# 建立task任务，[]里增加协程函数，并发数为5000
task0 = [clientGL(x) for x in range(concurrencyNum)]
# 运行事件循环
try:
    loop.run_until_complete(asyncio.wait(task0))
except:
    loop.close()

print("End time:" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
