import asyncio
import time
import base64
from gzip import decompress

# 定义协程函数，标志为async，await需要asyncio一起使用
async def clientGL(x):
    while 1:
        # 与服务器建立连接
        # connect = asyncio.open_connection('192.168.1.111', 6109)
        connect = asyncio.open_connection('120.204.202.101', 8691)
        reader, writer = await connect
        user = 'cmcc123'
        pwd = ':cmcc_123'
        mountpoint = 'source3'
        EncryptionStr = base64.b64encode(str.encode(user + pwd))
        # print(EncryptionStr)
        header = 'GET /' + mountpoint + ' HTTP/1.1\r\nUser-Agent: NTRIP ZHDGPS\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic ' + bytes.decode(EncryptionStr) + '\r\n\r\n'
        # 获取发送时间
        writer.write(header.encode('utf-8'))
        await writer.drain()
        # 接收服务器返回的登录信息
        line = await reader.readline()
        # print(line)
        if line == b'\r\n':
            break
        result = line.decode('utf-8').rstrip()
        print(result)
        # 返回信息为 ICY 200 OK 时，发送GGA数据
        if result == 'ICY 200 OK':
            while 1:
                # 获取不同时间段的GGA，并转换为字节流
                a = time.strftime('%H%M%S.%S', time.localtime(time.time()))
                GGA = '$GPGGA,' + a + ',3114.67923534,N,12135.54812367,E,1,24,0.6,43.580,M,-6.251,M,,*47'
                GGA = str.encode(GGA)
                # print(GGA)
                # 发送GGA，方法同Socket.sendall(GGA)
                writer.write(GGA)
                await writer.drain()
                # 接收差分数据，方法同Socket.recv(1024)
                Msg = await reader.read(1024)
                # 打印差分数据，根据需要选择是否屏蔽
                print(Msg)
                # print(decompress(Msg).decode('utf-8'))
                # print(str(Msg))
                # print(type(str(Msg)))
                #
                await asyncio.sleep(1)
        else:
            print("Error")
            continue
    writer.close()

# 创建一个默认的事件循环
loop = asyncio.get_event_loop()
# 建立task任务，[]里增加协程函数，并发数为5000
task0 = [clientGL(x) for x in range(500)]
# 运行事件循环
loop.run_until_complete(asyncio.wait(task0))
loop.close()