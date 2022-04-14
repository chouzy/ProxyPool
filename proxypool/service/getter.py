# -*- coding: UTF-8 -*-
# @author: admin
# @createTime: 2022/4/14 10:09 
# @description:
from loguru import logger

from config.setting import NUMBER_MAX
from proxypool.spiders import __all__ as spider_cls
from proxypool.storages.redis_db import RedisClient


class Getter(object):

    def __init__(self):
        self.redis_db = RedisClient()
        self.spider_cls = spider_cls
        self.crawlers = [spider_cls() for spider_cls in self.spider_cls]

    def is_full(self):
        """
        代理池是否已满
        :return:
        """
        return self.redis_db.count() > NUMBER_MAX

    def run(self):
        """
        run
        :return:
        """
        if self.is_full():
            return
        for crawler in self.crawlers:
            logger.info(f'spider: "{crawler}" to get proxy')
            for proxy in crawler.crawl():
                self.redis_db.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
