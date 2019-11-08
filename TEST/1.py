import pymysql
host = '192.168.238.133'
port = 3306
user = 'root'
password = '123456'
db = 'test'
pymysql.connect(host=host, port=port, user=user, passwd=password, db=db)