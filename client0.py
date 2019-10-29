from base64 import b64encode
import socket
def clientGL(x):
    while 1:
        # 与服务器建立连接
        # connect = asyncio.open_connection('192.168.1.111', 6109)
        connect = open_connection('120.204.202.101', 8691)
        reader, writer = await connect
        user = 'cmcc123'
        pwd = ':cmcc_123'
        mountpoint = 'source3'
        EncryptionStr = b64encode(str.encode(user + pwd))
        # print(EncryptionStr)
        header = 'GET /' + mountpoint + ' HTTP/1.1\r\nUser-Agent: NTRIP ZHDGPS\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic ' + bytes.decode(EncryptionStr) + '\r\n\r\n'
        # 获取发送时间