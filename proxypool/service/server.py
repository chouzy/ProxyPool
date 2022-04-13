# -*- coding: UTF-8 -*-
# @Project ：ProxyPool 
# @File    ：server.py
# @Date    ：2022/4/11 10:47

from flask import Flask, g

from config.setting import APP_DEBUG, API_HOST, API_PORT
from proxypool.storages.redis_db import RedisClient

__all__ = ['app']
app = Flask(__name__)

app.debug = APP_DEBUG


def get_conn() -> RedisClient:
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index() -> str:
    """
    默认界面
    :return:
    """
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_random() -> str:
    """
    获取随机代理
    :return:
    """
    conn = get_conn()
    return conn.random().string()


@app.route('/all')
def get_all() -> str:
    """
    获取所有代理
    :return:
    """
    conn = get_conn().all()
    proxies = ''
    for proxy in conn:
        proxies += proxy.string() + '\n'
    return proxies


@app.route('/count')
def get_count() -> str:
    """
    获取代理数量
    :return:
    """
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)


