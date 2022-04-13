# -*- coding: UTF-8 -*-
# @Project ：ProxyPool 
# @File    ：run.py
# @Date    ：2022/4/11 14:44

import argparse

from proxypool.main import ProxyPoolMain

parser = argparse.ArgumentParser(description='ProxyPool')
parser.add_argument('--processor', type=str, help='you can choose one from tester, getter and server')
args = parser.parse_args()

if __name__ == '__main__':
    # if processor set, just run it
    if args.processor:
        getattr(ProxyPoolMain(), f'run_{args.processor}')()
    else:
        ProxyPoolMain().run()
