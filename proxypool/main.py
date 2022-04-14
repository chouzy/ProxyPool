import multiprocessing
import time

from loguru import logger

from config.setting import IS_WINDOWS, START_TESTER, START_GETTER, START_SERVER, CYCLE_TESTER, CYCLE_GETTER, API_HOST, \
    API_PORT
from proxypool.service.getter import Getter
from proxypool.service.server import app
from proxypool.service.tester import Tester

if IS_WINDOWS:
    multiprocessing.freeze_support()

tester_process, getter_process, server_process = None, None, None


class ProxyPoolMain(object):
    """
    调度器
    """

    def run_tester(self, cycle=CYCLE_TESTER):
        """
        start tester
        :param cycle:
        :return:
        """
        if not START_TESTER:
            logger.info('tester not enabled, exit')
            return
        tester = Tester()
        loop = 0
        while True:
            logger.debug(f'tester loop {loop} start...')
            tester.run()
            loop += 1
            time.sleep(cycle)

    def run_getter(self, cycle=CYCLE_GETTER):
        """
        start getter
        :param cycle:
        :return:
        """
        if not START_GETTER:
            logger.info('getter not enabled, exit')
            return
        getter = Getter()
        loop = 0
        while True:
            logger.debug(f'getter loop {loop} start...')
            getter.run()
            loop += 1
            time.sleep(cycle)

    def run_server(self):
        """
        start server
        :return:
        """
        if not START_SERVER:
            logger.info('server not enabled, exit')
            return
        app.run(host=API_HOST, port=API_PORT)

    def run(self):
        global tester_process, getter_process, server_process
        try:
            logger.info('starting proxypool...')
            if START_TESTER:
                tester_process = multiprocessing.Process(target=self.run_tester)
                logger.info(f'starting tester, pid {tester_process.pid}...')
                tester_process.start()

            if START_GETTER:
                getter_process = multiprocessing.Process(target=self.run_getter)
                logger.info(f'starting getter, pid {getter_process.pid}...')
                getter_process.start()

            if START_SERVER:
                server_process = multiprocessing.Process(target=self.run_server)
                logger.info(f'starting server, pid {server_process.pid}...')
                server_process.start()

            tester_process and tester_process.join()
            getter_process and getter_process.join()
            server_process and server_process.join()
        except Exception as e:
            logger.error(f'an exception occurred in the proxypool, and err message is: {e}')
        finally:
            # must call join method before calling is_alive
            tester_process and tester_process.join()
            getter_process and getter_process.join()
            server_process and server_process.join()
            logger.info(
                f'tester is {"alive" if START_TESTER and tester_process.is_alive() else "dead"}')
            logger.info(
                f'getter is {"alive" if START_GETTER and getter_process.is_alive() else "dead"}')
            logger.info(
                f'server is {"alive" if START_SERVER and server_process.is_alive() else "dead"}')
            logger.info('proxy terminated')


if __name__ == '__main__':
    pro = ProxyPoolMain()
    pro.run()
