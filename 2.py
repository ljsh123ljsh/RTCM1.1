import asyncio
import socket

async def con():
    connect = asyncio.open_connection('192.168.130.52', 8201)
    reader, writer = await connect
    header = 'GET /source3' + ' HTTP/1.1\r\nUser-Agent: NTRIP ZHDGPS\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic ' + 'cmcc123'+ ':cmcc_123' + '\r\n\r\n'
    writer.write(header.encode())
    await writer.drain()
    line = await reader.readline()
    if line.deccode() == '\r\n':
        print('rrr'*5)
    print('header > {}'.format( line.decode().rstrip()))
    writer.close()
if __name__ == '__main__':
    con()


host_list = ['www.shiyanlou.com', 'www.sohu.com', 't.tt']   # 主机列表
loop = asyncio.get_event_loop()                             # 事件循环
tasks = asyncio.wait([wget(host) for host in host_list])    # 任务收集器
loop.run_until_complete(tasks)                              # 阻塞运行任务
loop.close()                                                # 关闭事件循环