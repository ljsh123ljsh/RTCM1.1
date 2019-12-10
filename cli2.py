import asyncio
import time
from base64 import b64encode
from binascii import b2a_hex
from random import random
from random import choice
from configparser import ConfigParser
import pika


def genGGA(hhddss):
    B0 = 3107.67923534
    L0 = 12131.54812367
    i = 1
    while i:
        B = round(B0 + random() * locaion_range * choice([1, -1]), 7)
        L = round(L0 + random() * locaion_range * choice([1, -1]), 7)
        GGA = '$GPGGA,' + str(hhddss) + ',' + str(B) + ',N,' + str(L) + ',E,1,24,0.6,43.580,M,-6.251,M,,*47'
        yield GGA, i


async def rabbit(Msg):
    channel.basic_publish(exchange=ex, routing_key='cc', body=Msg)

async def login():
    connect = asyncio.open_connection(host, port)
    reader, writer = await connect
    EncryptionStr = b64encode(str.encode(user + ':' + password))
    header = 'GET /' + mountpoint + ' HTTP/1.1\r\nUser-Agent: NTRIP ZHDGPS\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic ' + bytes.decode(
        EncryptionStr) + '\r\n\r\n'
    writer.write(header.encode())
    await writer.drain()
    line = await reader.readline()
    # print(line)
    if line == b'ICY 200 OK\r\n':
        return reader, writer


async def sendgga(reader, writer):
    hhddss = time.strftime('%H%M%S', time.localtime(time.time()))
    hhddss = int(hhddss) - 80000
    if hhddss < 0:
        hhddss = hhddss + 120000
    GGA, No = next(genGGA(hhddss))
    # 获取不同时间段的GGA，并转换为字节流
    GGA = str.encode(GGA)
    i = 1
    while i:
        # 发送GGA，方法同Socket.sendall(GGA)
        print('---' + str(i))
        i += 1
        if writer.is_closing():
            await login()
        writer.write(GGA)
        await writer.drain()
        Msg = await reader.read(1500)
        Msg = b2a_hex(Msg).decode('utf-8')
        # 打印差分数据，根据需要选择是否屏蔽
        await rabbit(Msg)
        await asyncio.sleep(1)

async def loop():
    task = [login() for i in range(50)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(task))
    await asyncio.wait(simulator_number/50)


if __name__ == '__main__':
    cf = ConfigParser()

    cf.read('conf.ini', encoding='ANSI')
    host = cf.get('ntripcaster', 'IP')
    print(host)
    port = int(cf.get('ntripcaster', 'port'))
    user = cf.get('ntripcaster', 'user')
    password = cf.get('ntripcaster', 'password')
    mountpoint = cf.get('ntripcaster', 'mountpoint')
    locaion_range = float(cf.get('client', 'range'))
    simulator_number = int(cf.get('client', 'clientnumber'))
    credentials = pika.PlainCredentials(cf.get('rabbitmq', 'user'), cf.get('rabbitmq', 'password'))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=cf.get('rabbitmq', 'host'), port=int(cf.get('rabbitmq', 'port')),
                                  credentials=credentials))
    channel = connection.channel()
    ex = cf.get('rabbitmq', 'exchange')
    channel.exchange_declare(exchange=ex, exchange_type='fanout')
    frequency = int(cf.get('client', 'frequency'))
    totaltime = int(cf.get('client', 'totaltime'))


