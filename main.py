# -*- coding: UTF-8 -*-
from config import PERSISTENCE
from spider.crawl_xici import XiCi

if PERSISTENCE['type'] == 'redis':
    from persistence.redis_impl import Redis as persister
elif PERSISTENCE['type'] == 'mongo':
    from persistence.mongo_impl import Mongo as persister
else:
    from persistence.redis_impl import Redis as persister

spider = XiCi()
persister = persister()
for item in spider.generator(anonymity='transparent'):
    print(item)
    persister.add(item)
