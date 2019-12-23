import socket

s = socket.socket()
s.connect(('192.168.111.126', 8105))
header = 'GET /' + 'RTCM33GREC2' + ' HTTP/1.1\r\nUser-Agent: NTRIP ZHDGPS\r\nAccept: */*\r\nConnection: close\r\nAuthorization: Basic ' + 'Y21jYzEyMzpjbWNjXzEyMw==' + '\r\n\r\n'
header = header.encode()
s.send(header)
c = s.recv(1024)
print(c)