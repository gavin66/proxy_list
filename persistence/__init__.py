# -*- coding: UTF-8 -*-
import config

if config.PERSISTENCE['type'] == 'redis':
    from persistence.redis_impl import Redis as p
elif config.PERSISTENCE['type'] == 'mongo':
    from persistence.mongo_impl import Mongo as p
else:
    from persistence.redis_impl import Redis as p
persister = p()


def worker(queue_persistence):
    while True:
        persister.add(queue_persistence.get())
