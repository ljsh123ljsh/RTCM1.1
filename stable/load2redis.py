import json
from DB import MYSQL, REDIS

def main():
    # r = db.REDIS
    r = REDIS.REDIS
    connection = MYSQL.MYSQL
    # print(type(connection))
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
            value = {
                cols[1][0]: result[1],
                cols[2][0]: result[2],
                cols[3][0]: result[3],
                cols[4][0]: result[4]
            }
            value = json.dumps(value)
            r.hset(table, result[0], value)
if __name__ == '__main__':
    main()
