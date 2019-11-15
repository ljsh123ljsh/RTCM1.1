import pymysql
import redis
import json

def main():
    r = redis.StrictRedis(host='49.233.166.39', port=6379, db=10)
    connection = pymysql.connect(host='49.233.166.39', port=3306, user='root', password='123456', db='singal')
    cursor = connection.cursor()
    cursor.execute("show tables")

    table_list = [tuple[0] for tuple in cursor.fetchall()]
    for table in table_list:
        sql = 'select * from ' + table
        cursor.execute(sql)
        results = cursor.fetchall()
        # print(results)
        cursor.execute('SHOW COLUMNS FROM '+table)
        cols = cursor.fetchall()
        print(table)
        for result in results:
            # print(cols[1][0])
            value = {
                cols[1][0]: result[1],
                cols[2][0]: result[2],
                cols[3][0]: result[3],
                cols[4][0]: result[4]
            }
            value = json.dumps(value)
            r.hset(table, result[0], value)
