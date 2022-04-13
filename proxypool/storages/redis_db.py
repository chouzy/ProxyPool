from random import choice
from typing import Union, List, Tuple, Any

from redis import StrictRedis

from config.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB, REDIS_KEY, SCORE_MAX, SCORE_MIN, SCORE_INIT
from proxypool.comm.proxy import Proxy
from proxypool.comm.utils import to_proxy_object


class RedisClient(object):
    """
    设置 redis 链接及操作
    """

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, psw=REDIS_PASSWORD, db=REDIS_DB, **kwargs):
        """
        初始化 redis 链接
        :param host: ‘127.0.0.1’
        :param port: 6379
        :param psw: ‘root’
        :param db: 0
        :param kwargs:
        """
        self.db = StrictRedis(host=host, port=port, password=psw, db=db, **kwargs)

    def add(self, proxy: Proxy, score=SCORE_INIT) -> None:
        """
        添加 proxy 到 redis
        :param proxy: Proxy()
        :param score: 10
        :return:
        """
        self.db.zadd(REDIS_KEY, {proxy.string(): score})

    def random(self) -> Proxy:
        """
        生成随机 proxy
        :return: Proxy()
        """
        # 获取 score == 100 的 proxy
        proxies = self.db.zrangebyscore(REDIS_KEY, SCORE_MAX, SCORE_MAX)
        if len(proxies):
            return to_proxy_object(choice(proxies))
        # 获取 score 排名前 100 的 proxy
        proxies = self.db.zrevrange(REDIS_KEY, SCORE_MIN, SCORE_MAX)
        if len(proxies):
            return to_proxy_object(choice(proxies))
        raise Exception('no proxy in proxypool')

    def all(self) -> List[Proxy]:
        """
        获取所有 proxy
        :return: [Proxy()]
        """
        return to_proxy_object(self.db.zrangebyscore(REDIS_KEY, SCORE_MIN, SCORE_MAX))

    def batch(self, cursor, count) -> Tuple[Any, Union[List[Proxy], Proxy]]:
        """
        迭代 proxy_pool
        :param cursor:
        :param count:
        :return:
        """
        cursor, proxies = self.db.zscan(REDIS_KEY, cursor, count=count)
        return cursor, to_proxy_object([i[0] for i in proxies])

    def count(self) -> int:
        """
        统计代理池中代理的数量
        :return: number of proxy
        """
        return self.db.zcard(REDIS_KEY)

    def score_to_max(self, proxy: Proxy, score=SCORE_MAX) -> None:
        """
        设置 score = 100
        :param proxy: Proxy()
        :param score: 100
        :return:
        """
        self.db.zadd(REDIS_KEY, {proxy.string(): score})

    def score_decrease(self, proxy: Proxy) -> None:
        """
        设置 score = score-1
        :param proxy: Proxy()
        :return:
        """
        self.db.zincrby(REDIS_KEY, -1, proxy.string())
        if self.db.zscore(REDIS_KEY, proxy.string()) <= SCORE_MIN:
            self.db.zrem(REDIS_KEY, proxy.string())


if __name__ == '__main__':
    redis_db = RedisClient()
    res1 = redis_db.all()
    print(res1)
    res2 = redis_db.random()
    print(res2)
