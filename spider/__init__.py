# -*- coding: UTF-8 -*-
from spider.crawl_xici import XiCi
from spider.crawl_nianshao import NianShao
from persistence import persister
import config
import time


def worker(queue_verification):
    spiders = [XiCi(), NianShao()]
    page = 1
    while page < 16:
        for spider in spiders:
            for proxy in spider.generator(page):
                if persister.handler().zcount('index_speed', '-inf', '+inf') > config.PROXY_STORE_NUM:
                    time.sleep(config.PROXY_FULL_SLEEP_SEC)
                elif queue_verification.full():
                    time.sleep(0.5)
                else:
                    queue_verification.put(proxy)
        if page == 15:
            page = 1
        else:
            page += 1
