# -*- coding: UTF-8 -*-
from persistence.base import Base
from redis import Redis as pyRedis
from config import PERSISTENCE


class Redis(Base):
    def __init__(self):
        # redis 操作客户端
        self._client = pyRedis.from_url(PERSISTENCE['url'])
        # 可搜索项
        self._index_keys = ('anonymity', 'protocol')

    def get_keys(self, query=None):
        if 'ip' in query and query['ip']:
            return [x.decode('utf8') for x in self._client.keys('proxy_%s:%s_%s' % (
                query['ip'], query['port'] if 'port' in query and query['port'] else '*',
                query['protocol'] if 'protocol' in query and query['protocol'] else '*'))]
        index_keys = {'index_%s_%s' % (k, v) for k, v in query.items() if k in self._index_keys}
        if index_keys:
            return [v.decode('utf8') for v in self._client.sinter(keys=index_keys)]
        return dict()

    def list(self, count=1, query=None, columns=None):
        query_list = list()
        if query:
            for k, v in query.items():
                if k in self._index_keys:
                    query_list.append('index_%s_%s' % (k, v))
            keys = list(self._client.sinter(query_list))
            keys.sort(key=lambda x: float(self._client.zscore('index_speed', x)))
            if isinstance(count, int):
                keys = keys[:count]
        else:
            start = 0
            if isinstance(count, str):
                count = None
                start = None
            keys = list(self._client.zrangebyscore('index_speed', '-inf', '+inf', start=start, num=count))
        proxies = []
        for key in keys:
            proxy = self._client.hgetall(key)
            if isinstance(columns, tuple) and len(columns):
                x = {}
                for k in columns:
                    if k.encode('utf-8') in proxy.keys():
                        x[k] = proxy[k.encode('utf-8')].decode('utf-8')
                proxies.append(x)
            elif isinstance(columns, str) and columns == 'all':
                # ip, port, country, address, anonymity, protocol, speed
                proxies.append({x.decode('utf-8'): y.decode('utf-8') for x, y in proxy.items()})
            else:
                proxies.append(
                    (proxy[b'ip'].decode('utf-8'), proxy[b'port'].decode('utf-8'))
                )
        return proxies

    def add(self, data):
        # 存储代理
        proxy_key = 'proxy_%s:%s_%s' % (data['ip'], data['port'], data['protocol'])
        self._client.hmset(proxy_key, data)
        # 存储索引,以便搜索
        # 得分
        self._client.zadd('index_speed', proxy_key, data['speed'])
        for key in self._index_keys:
            self._client.sadd('index_%s_%s' % (key, data[key]), proxy_key)

    def update(self, data):
        """
        更新操作,因为已经存在此键的索引,所以只需更新他的 hash 类型中的值和速度 zset 中的值
        :param data:
        :return:
        """
        proxy_key = 'proxy_%s:%s_%s' % (data['ip'], data['port'], data['protocol'])
        self._client.hmset(proxy_key, data)
        self._client.zrem('index_speed', proxy_key)
        self._client.zadd('index_speed', proxy_key, data['speed'])

    def delete(self, data):
        proxy_key = 'proxy_%s:%s_%s' % (data['ip'], data['port'], data['protocol'])
        self._client.delete(proxy_key)
        self._client.zrem('index_speed', proxy_key)
        for key in self._index_keys:
            self._client.srem('index_%s_%s' % (key, data[key]), proxy_key)

    def handler(self):
        return self._client
