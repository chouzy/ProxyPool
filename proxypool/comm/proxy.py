from attr import attr, attrs


@attrs
class Proxy(object):
    """
    定义代理对象
    """
    host = attr(type=str, default=None)
    port = attr(type=str, default=None)

    def __str__(self):
        return f'{self.host}:{self.port}'

    def string(self) -> str:
        return self.__str__()
