# -*- coding: UTF-8 -*-
import config
import gevent
import availability.check


def worker(queue_verification, queue_persistence):
    while True:
        spawns = list()
        for i in range(config.COROUTINE_NUM):
            proxy = queue_verification.get()
            spawns.append(gevent.spawn(availability.check.handle, 'http', proxy, queue_persistence))
            spawns.append(gevent.spawn(availability.check.handle, 'https', proxy, queue_persistence))
        gevent.joinall(spawns)
