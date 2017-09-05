# -*- coding: UTF-8 -*-
import config
import gevent
import availability.check
from persistence import persister
import time


def crawl_worker(queue_verification, queue_persistence):
    """
    爬取下来的代理检测可用性的进程
    :param queue_verification: 待验证代理队列
    :param queue_persistence: 已验证待保存代理队列
    :return:
    """
    while True:
        spawns = list()
        for i in range(config.COROUTINE_NUM):
            proxy = queue_verification.get()
            spawns.append(gevent.spawn(availability.check.crawl_handle, 'http', proxy, queue_persistence))
            spawns.append(gevent.spawn(availability.check.crawl_handle, 'https', proxy, queue_persistence))
        gevent.joinall(spawns)


def store_worker():
    """
    已保存的代理每隔一段时间重新验证可用性的进程
    """
    while True:
        all_proxies = persister.list(count='all', columns='all')
        spawns = list()
        for proxy in all_proxies:
            if proxy['protocol'] == 'http':
                spawns.append(gevent.spawn(availability.check.store_handle, 'http', proxy, persister))
            else:
                spawns.append(gevent.spawn(availability.check.store_handle, 'https', proxy, persister))
            if len(spawns) == config.COROUTINE_NUM:
                gevent.joinall(spawns)
                spawns.clear()

        gevent.joinall(spawns)
        spawns.clear()
        time.sleep(config.PROXY_STORE_CHECK_SEC)
