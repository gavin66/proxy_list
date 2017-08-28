# -*- coding: UTF-8 -*-
from spider.crawl_xici import XiCi
import time


def worker(queue_verification):
    spider = XiCi()
    for proxy in spider.transparent():
        while True:
            if queue_verification.full():
                time.sleep(0.2)
            else:
                queue_verification.put(proxy)
                break

