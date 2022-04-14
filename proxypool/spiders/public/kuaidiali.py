# -*- coding: UTF-8 -*-
# @author: admin
# @CreateTime: 2022/4/14 9:36 
# @Description:

from loguru import logger
from pyquery import PyQuery as pq

from proxypool.comm.proxy import Proxy
from proxypool.spiders.base import BaseSpider

URL = 'https://www.kuaidaili.com/free/inhaq/{page}/'
PAGE_MAX = 1


class KuaidailiSpider(BaseSpider):
    """
    快代理
    """

    urls = [URL.format(page=page) for page in range(1, PAGE_MAX + 1)]

    def parse(self, html: str):
        """
        重写父类 parse 方法
        :param html:
        :return:
        """
        doc = pq(html)
        for item in doc('table tr').items():
            td_ip = item.find('td[data-title="IP"]').text()
            td_port = item.find('td[data-title="PORT"]').text()
            if td_ip and td_port:
                logger.info(f'proxy is get, proxy: {td_ip}:{td_port}')
                yield Proxy(host=td_ip, port=td_port)


if __name__ == '__main__':
    kuaidaili = KuaidailiSpider()
    for proxy in kuaidaili.crawl():
        print(proxy)
