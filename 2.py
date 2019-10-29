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
    print('{} header > {}'.format(host, line.decode().rstrip()))
