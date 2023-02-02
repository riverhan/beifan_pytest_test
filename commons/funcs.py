"""
@Filename:   commons/funcs
@Author:      北凡
@Time:        2023/2/1 20:26
@Describe:    ...
"""
import time
import urllib.parse
from commons.databases import db


def url_unquote(s: str) -> str:
    return urllib.parse.unquote(s)


def time_str():
    return str(time.time())


def add(a, b) -> str:
    return str(int(a) + int(b))


def sql(s: str) -> str:
    res = db.execute_sql(s)  # 执行sql

    return res[0]
