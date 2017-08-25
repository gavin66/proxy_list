# -*- coding: UTF-8 -*-
import gevent
import time
import requests
import json
import config
from gevent import monkey

monkey.patch_all()


def worker(queue_verification, queue_persistence):
    while True:
        spawns = list()
        for i in range(config.COROUTINE_NUM):
            proxy = queue_verification.get()
            spawns.append(gevent.spawn(handle, 'http', proxy, queue_persistence))
            spawns.append(gevent.spawn(handle, 'https', proxy, queue_persistence))
        gevent.joinall(spawns)


def handle(protocal, proxy, queue_persistence):
    if protocal is 'http':
        http, h_anonymity, h_interval = check('http://httpbin.org/get', proxy)
        if http:
            proxy['protocol'] = 'http'
            proxy['anonymity'] = h_anonymity
            proxy['speed'] = h_interval
            queue_persistence.put(proxy)
    elif protocal is 'https':
        https, hs_anonymity, hs_interval = check('https://httpbin.org/get', proxy)
        if https:
            proxy['protocol'] = 'https'
            proxy['anonymity'] = hs_anonymity
            proxy['speed'] = hs_interval
            queue_persistence.put(proxy)


def check(u, p):
    try:
        start_point = time.time()
        response = requests.get(u, proxies={
            'http': 'http://%s:%s' % (p['ip'], p['port']),
            'https': 'http://%s:%s' % (p['ip'], p['port'])
        }, **{'timeout': 5})
        if response.ok:
            interval = round(time.time() - start_point, 2)
            res_json = json.loads(response.text)
            ip = res_json['origin']
            if ',' in ip:
                anonymity = 'transparent'
            else:
                anonymity = 'anonymous'
            return True, anonymity, interval
        else:
            return False, False, False
    except Exception:
        return False, False, False
