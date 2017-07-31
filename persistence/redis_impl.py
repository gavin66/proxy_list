# -*- coding: UTF-8 -*-
from persistence.base import Base
from redis import Redis as pyRedis
from config import PERSISTENCE


class Redis(Base):
    def __init__(self):
        self._client = pyRedis.from_url(PERSISTENCE['url'])

    def list(self):
        pass

    def get(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def add(self):

        self._client.set('far', 'bor')

    def handler(self):
        return self._client


if __name__ == '__main__':
    redis = Redis()
    handler = redis.handler()
