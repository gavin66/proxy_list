# -*- coding: UTF-8 -*-
from persistence.base import Base
from redis import Redis as pyRedis
from config import PERSISTENCE


class Redis(Base):
    def __init__(self):
        # redis 操作客户端
        self._client = pyRedis.from_url(PERSISTENCE['url'])

        # 可搜索项
        self._index_keys = ('anonymity', 'protocol', 'speed')

    def list(self):
        pass

    def get(self):
        pass

    def add(self, data):
        # 存储代理
        proxy_key = 'proxy_%s:%s_%s' % (data['ip'], data['port'], data['protocol'])
        self._client.hmset(proxy_key, data)

        # 存储索引,以便搜索
        for key in self._index_keys:
            if key == 'speed':
                self._client.zadd('index_speed', proxy_key, data['speed'])
            else:
                self._client.sadd('index_%s_%s' % (key, data[key]), proxy_key)

    def update(self):
        pass

    def delete(self):
        pass

    def handler(self):
        return self._client


if __name__ == '__main__':
    redis = Redis()
    handler = redis.handler()
    print(handler.set('a', 'b'))
