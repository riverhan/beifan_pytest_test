import logging

import pymysql as MySQLdb


class DBServer:
    def __init__(self, *args, **kwargs):
        self.db = MySQLdb.connect(*args, **kwargs)
        self.c = self.db.cursor()  # 创建新的会话

    def execute_sql(self, sql):
        logging.info(f"{sql=}")
        self.c.execute(sql)  # 执行sql命令

        res = self.c.fetchone()  # 返回单行结果
        # res = self.c.fetchall()  # 返回多行结果
        return res


db = DBServer(
    host="101.34.221.219",  # IP
    port=13306,  # 端口
    user="dev",  # 用户名
    password="dev_My_ShopPx",  # 密码
    database="beifan_db",  # 库名
)

if __name__ == '__main__':
    res = db.execute_sql("select count(1) from report where author='beifan_88'")
    print(res)