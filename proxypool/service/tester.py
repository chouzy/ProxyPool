# -*- coding: UTF-8 -*-
# @Project ：ProxyPool 
# @File    ：tester.py
# @Date    ：2022/4/11 9:01

import asyncio

import aiohttp
from loguru import logger

from config.setting import TEST_URL, TEST_TIMEOUT, TEST_BATCH
from proxypool.comm.proxy import Proxy
from proxypool.storages.redis_db import RedisClient


class Tester(object):
    def __init__(self):
        """
        初始化
        """
        self.redis_db = RedisClient()
        self.loop = asyncio.get_event_loop()

    async def test(self, proxy: Proxy) -> None:
        """
        测试代理是否可用
        :param proxy: Proxy()
        :return:
        """
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            try:
                async with session.get(url=TEST_URL, proxy=f'http://{proxy.string()}',
                                       timeout=TEST_TIMEOUT) as response:
                    if response.status == 200:
                        logger.info(f'"{proxy.string()}" status is 200, and set the score to 100.')
                        self.redis_db.score_to_max(proxy)
                    else:
                        logger.info(f'"{proxy.string()}" status is err, and score decrease.')
                        self.redis_db.score_decrease(proxy)
            except Exception as e:
                logger.error(f'{proxy.string()} request exception, and error message is: {e}')

    @logger.catch
    def run(self):
        logger.info('stating tester...')
        count = self.redis_db.count()
        logger.debug(f'{count} proxies to test')
        cursor = 0
        while True:
            logger.debug(f'testing proxies use cursor {cursor}, count {TEST_BATCH}')
            cursor, proxies = self.redis_db.batch(cursor, count=TEST_BATCH)
            if proxies:
                tasks = [self.test(proxy) for proxy in proxies]
                self.loop.run_until_complete(asyncio.wait(tasks))
            if not cursor:
                break


if __name__ == '__main__':
    tes = Tester()
    tes.run()
