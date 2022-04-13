from typing import Generator, Any

import requests
from fake_headers import Headers
from loguru import logger
from pyquery import PyQuery as pq

from proxypool.comm.proxy import Proxy
from proxypool.storages.redis_db import RedisClient


class KuaidailiSpider(object):
    """
    快代理爬虫
    """
    URL = 'https://www.kuaidaili.com/free/inha/{page}/'
    PAGE_MAX = 1

    redis_db = RedisClient()

    def get_html(self) -> Generator[str, Any, None]:
        """
        请求网页 URL
        :return:
        """
        for page in range(1, self.PAGE_MAX + 1):
            response = requests.get(self.URL.format(page=page), headers=Headers(headers=True).generate())
            if response.status_code == 200:
                logger.info(f'URL status code is 200, URL: {self.URL.format(page=page)}')
                yield response.text
            else:
                logger.error(f'The URL request failed, URL: {self.URL.format(page=page)}')
                continue

    def parse(self, data) -> Generator[Proxy, Any, None]:
        """
        解析页面
        :param data:
        :return:
        """
        doc = pq(data)
        for item in doc('table tr').items():
            td_ip = item.find('td[data-title="IP"]').text()
            td_port = item.find('td[data-title="PORT"]').text()
            if td_ip and td_port:
                logger.info(f'proxy is get, proxy: {td_ip}:{td_port}')
                yield Proxy(host=td_ip, port=td_port)

    def add_proxy_to_redis(self, proxy: Proxy) -> None:
        """
        添加 Proxy 对象到 redis
        :param proxy:
        :return:
        """
        self.redis_db.add(proxy)

    def run(self) -> None:
        """
        启动爬虫
        :return:
        """
        for html in self.get_html():
            for proxy in self.parse(html):
                self.add_proxy_to_redis(proxy)


if __name__ == '__main__':
    kuai = KuaidailiSpider()
    kuai.run()
