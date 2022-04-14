# -*- coding: UTF-8 -*-
# @Project ：ProxyPool 
# @File    ：base.py
# @Date    ：2022/4/13 17:17
import time

import requests
import urllib3
from fake_headers import Headers
from loguru import logger
from retrying import retry, RetryError

from config.setting import GET_TIMEOUT
from proxypool.comm.proxy import Proxy

urllib3.disable_warnings()


class BaseSpider(object):
    urls = []

    @retry(stop_max_attempt_number=3, retry_on_result=lambda x: x is None, wait_fixed=2000)
    def request_url(self, url: str, **kwargs):
        """
        请求 url 获取页面 html
        :param url: url
        :param kwargs:
        :return:
        """
        try:
            header = Headers(headers=True).generate()
            kwargs.setdefault('headers', header)
            kwargs.setdefault('verify', False)
            kwargs.setdefault('timeout', GET_TIMEOUT)
            response = requests.get(url, **kwargs)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.text
        except requests.ConnectionError:
            return

    def parse(self, html: str):
        """
        解析 HTML, 留给子类重写
        """
        yield Proxy

    def process(self, url: str, html: str):
        """
        处理 HTML
        """
        for proxy in self.parse(html):
            logger.info(f'Get {proxy} from URL: {url}')
            yield proxy

    def crawl(self):
        """
        爬虫
        :return:
        """
        try:
            for url in self.urls:
                logger.info(f'The request starts, the request URL is: {url}')
                html = self.request_url(url)
                time.sleep(.5)
                yield from self.process(url, html)
        except RetryError:
            logger.error(f'URL: "{url}" request failed, please check if the network or link is valid')
