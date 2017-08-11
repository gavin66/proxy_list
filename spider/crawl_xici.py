# -*- coding: UTF-8 -*-
from spider.crawl import Crawl
from lxml import etree
import time
import json
import requests


class XiCi(Crawl):
    def __init__(self):
        Crawl.__init__(self)

    def _transparent(self):
        url = 'http://www.xicidaili.com/nt/%u'
        done = False
        page = 1
        fail = 0
        while not done:
            text = self._text(url % page)
            if text is not None:
                proxies = self._parse(text)
                if proxies is not None:
                    for proxy in proxies:
                        proxy = self._connectable(proxy)
                        if isinstance(proxy, list):
                            for item in proxy:
                                yield item
                        elif isinstance(proxy, dict):
                            yield proxy
                    page += 1
                else:
                    fail += 1
            else:
                fail += 1
            # 如果失败大于5次,停止爬取
            if fail > 5 or page == 5:
                done = True

    def _anonymous(self):
        url = 'http://www.xicidaili.com/nn/%u'
        done = False
        page = 1
        fail = 0
        while not done:
            text = self._text(url % page)
            if text is not None:
                proxies = self._parse(text)
                if proxies is not None:
                    for proxy in proxies:
                        proxy = self._connectable(proxy)
                        if isinstance(proxy, list):
                            for item in proxy:
                                yield item
                        elif isinstance(proxy, dict):
                            yield proxy
                    page += 1
                else:
                    fail += 1
            else:
                fail += 1
            # 如果失败大于5次,停止爬取
            if fail > 5 or page == 5:
                done = True

    def _text(self, url):
        response = self._session.get(url, **self._request_kwargs)
        if response.ok:
            return response.text
        else:
            # TODO 使用代理重新尝试下载
            return None

    def _parse(self, text):
        proxies = list()
        root = etree.HTML(text)
        ip_list = root.xpath(".//*[@id='ip_list']/tr[position()>1]")

        if not ip_list:
            return None

        for item in ip_list:
            ip = item.xpath('./td[2]')[0].text
            port = item.xpath('./td[3]')[0].text

            # 国家
            try:
                country = item.xpath('./td[1]/img/@alt')[0]
            except IndexError:
                country = ''

            # 地址
            try:
                address = item.xpath('./td[4]/a')[0].text
            except IndexError:
                address = ''

            # 协议
            protocol = item.xpath('./td[6]')[0].text.lower()

            proxy = {
                'ip': ip,
                'port': port,
                'country': country,
                'address': address,
                'anonymity': '',  # anonymous transparent
                'protocol': protocol,  # http https http&https
                'speed': 0.00
            }

            proxies.append(proxy)

        return proxies

    def _connectable(self, proxy):
        """
        验证可连接性,返回此代理的类型等数据
        :param proxy:
        :return:
        """

        def check(u, p):
            try:
                start_point = time.time()
                response = requests.get(u, proxies={
                    'http': 'http://%s:%s' % (p['ip'], p['port']),
                    'https': 'http://%s:%s' % (p['ip'], p['port'])
                }, **self._request_kwargs)
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

        http, h_anonymity, h_interval = check('http://httpbin.org/get', proxy)
        https, hs_anonymity, hs_interval = check('https://httpbin.org/get', proxy)

        if http and https:
            proxy1 = proxy.copy()
            proxy2 = proxy.copy()
            proxy1['protocol'] = 'http'
            proxy1['anonymity'] = h_anonymity
            proxy1['speed'] = h_interval
            proxy2['protocol'] = 'https'
            proxy2['anonymity'] = hs_anonymity
            proxy2['speed'] = hs_interval
            proxy = [proxy1, proxy2]
        elif http:
            proxy['protocol'] = 'http'
            proxy['anonymity'] = h_anonymity
            proxy['speed'] = h_interval
        elif https:
            proxy['protocol'] = 'https'
            proxy['anonymity'] = hs_anonymity
            proxy['speed'] = hs_interval
        else:
            proxy = False

        return proxy

    def generator(self, anonymity='anonymous'):
        if anonymity is 'anonymous':
            return self._anonymous()
        elif anonymity is 'transparent':
            return self._transparent()
        else:
            return dict()

    def test(self):
        # self._parse(self._content('http://www.xicidaili.com/nn/1'))
        # for item in self.generator(anonymity='anonymous'):
        #     print(item)
        return self._connectable(proxy={
            'ip': '47.94.81.119',
            'port': '8888'
        })


if __name__ == '__main__':
    c = XiCi()
    # c.test()
    res = c.test()
    if res.ok:
        print(res.text)
    else:
        print('fail')
