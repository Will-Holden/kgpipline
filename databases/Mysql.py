import pymysql
from DBUtils.PooledDB import PooledDB
from settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
from core.Singleton import Singleton


class Mysql(metaclass=Singleton):
    def __init__(self, host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
                 passwd=MYSQL_PASSWORD, db=MYSQL_DB):
        self.pool = PooledDB(pymysql, 5,
                             host=host,
                             port=port,
                             user=user,
                             passwd=passwd,
                             db=db)

    def execute_as_gen(self, *sqls):
        conn = self.pool.connection()
        # conn.set
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            for sql in sqls:
                cursor.execute(sql)
            datas_source = cursor.fetchmany(100)
            while datas_source:
                datas = [data for data in datas_source]
                yield datas
                datas_source = cursor.fetchmany(100)
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    def execute(self, *sqls):
        conn = self.pool.connection()
        # conn.set
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        try:
            for sql in sqls:
                cursor.execute(sql)
            datas_source = cursor.fetchall()
            datas = [data for data in datas_source]
            return datas
        finally:
            conn.commit()
            cursor.close()
            conn.close()


if __name__ == '__main__':
    print(Mysql().execute("show databases;))
