# -*- coding: UTF-8 -*-
import multiprocessing
import config
import spider
import availability
import persistence
import web

# 进程间队列
# 爬取的代理
queue_verification = multiprocessing.Queue(config.COROUTINE_NUM)
# 待持久化的代理
queue_persistence = multiprocessing.Queue()

# 多进程列表
workers = list()
# 爬虫
workers.append(multiprocessing.Process(target=spider.worker, args=(queue_verification,)))
# 验证
workers.append(multiprocessing.Process(target=availability.worker, args=(queue_verification, queue_persistence)))
# 持久化
workers.append(multiprocessing.Process(target=persistence.worker, args=(queue_persistence,)))
# web api 服务
workers.append(multiprocessing.Process(target=web.worker))

for worker in workers:
    worker.start()

for worker in workers:
    worker.join()
