# -*- coding: UTF-8 -*-
from spider.crawl_xici import XiCi
from persistence import persister
import config
import time


def worker(queue_verification):
    spider = XiCi()
    for proxy in spider.generator():
        while True:
            if persister.handler().zcount('index_speed', '-inf', '+inf') > config.PROXY_STORE_NUM:
                time.sleep(config.PROXY_FULL_SLEEP_SEC)
            elif queue_verification.full():
                time.sleep(0.5)
            else:
                queue_verification.put(proxy)
                break

