# -*- coding: UTF-8 -*-
from spider.crawl_xici import XiCi
from persistence import db
import time


def worker(queue_verification):
    spider = XiCi()
    for proxy in spider.generator():
        while True:
            if db.handler().zcount('index_speed', '-inf', '+inf') > 200:
                time.sleep(60 * 3)
            elif queue_verification.full():
                time.sleep(0.5)
            else:
                queue_verification.put(proxy)
                break

