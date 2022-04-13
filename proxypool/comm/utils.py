from typing import Union, List

from proxypool.comm.proxy import Proxy


def to_proxy_object(data) -> Union[List[Proxy], Proxy]:
    """
    将数据转换为 Proxy 对象
    :param data:
    :return:
    """
    if isinstance(data, list):
        result = []
        for item in data:
            item = str(item, encoding='utf-8').strip()
            host, port = item.split(':')
            result.append(Proxy(host=host, port=int(port)))
        return result
    if isinstance(data, bytes):
        item = str(data, encoding='utf-8').strip()
        host, port = item.split(':')
        return Proxy(host=host, port=int(port))

# def is_host(data:str):
#     # '127.0.0.1'
#     hosts=data.strip().split(':')
#     for host in hosts:
#         if isinstance(host,int) and
