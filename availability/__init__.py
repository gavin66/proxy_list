# -*- coding: UTF-8 -*-
import config
import availability.check
import gevent
from gevent import monkey

monkey.patch_all()


def worker(queue_verification, queue_persistence):
    while True:
        spawns = list()
        for i in range(config.COROUTINE_NUM):
            proxy = queue_verification.get()
            spawns.append(gevent.spawn(availability.check.handle, 'http', proxy, queue_persistence))
            spawns.append(gevent.spawn(availability.check.handle, 'https', proxy, queue_persistence))
        gevent.joinall(spawns)
