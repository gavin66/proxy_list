# -*- coding: UTF-8 -*-
from gevent import monkey
monkey.patch_all()

import multiprocessing
import config
import spider
import availability
import persistence
import web

if __name__ == '__main__':
    # 进程间队列
    # 爬取的代理
    queue_verification = multiprocessing.Queue(config.COROUTINE_NUM)
    # 待持久化的代理
    queue_persistence = multiprocessing.Queue()

    # 多进程列表
    workers = list()
    # 爬虫
    workers.append(multiprocessing.Process(target=spider.worker, args=(queue_verification,)))
    # 爬取下来的代理验证
    workers.append(multiprocessing.Process(target=availability.crawl_worker, args=(queue_verification, queue_persistence)))
    # 已持久化的代理验证
    workers.append(multiprocessing.Process(target=availability.store_worker))
    # 持久化
    workers.append(multiprocessing.Process(target=persistence.worker, args=(queue_persistence,)))
    # web api 服务
    workers.append(multiprocessing.Process(target=web.worker))

    for worker in workers:
        worker.start()

    for worker in workers:
        worker.join()
