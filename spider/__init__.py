# -*- coding: UTF-8 -*-
from spider.crawl_xici import XiCi
from spider.crawl_kuai import Kuai
from persistence import persister
import config
import time


def worker(queue_verification):
    """
    工作进程,从各个源来爬取代理
    取消了 www.nianshao.me 的代理爬取,此网站应该是没人维护,已经挂了
    :param queue_verification:
    :return:
    """
    # 好的源排在前面优先被爬取
    spiders = [Kuai(), XiCi()]
    page = 1
    while page <= config.PAGE:
        for spider in spiders:
            for proxy in spider.generator(page):
                if persister.handler().zcount('index_speed', '-inf', '+inf') > config.PROXY_STORE_NUM:
                    time.sleep(config.PROXY_FULL_SLEEP_SEC)
                elif queue_verification.full():
                    time.sleep(1)
                else:
                    queue_verification.put(proxy)
        if page == config.PAGE:
            page = 1
        else:
            page += 1
