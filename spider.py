# -*- coding: UTF-8 -*-
import requests
from config import HEADER
from lxml import etree


class Spider(object):
    def __init__(self):
        self._proxies = set()
        self._parser = Parser()

    def crawl(self):
        text = self.download()
        attr = {
            'urls': ['http://www.66ip.cn/%s.html' % n for n in ['index'] + list(range(2, 12))],
            'type': 'xpath',
            'pattern': ".//*[@id='main']/div/div[1]/table/tr[position()>1]",
            'position': {'ip': './td[1]', 'port': './td[2]', 'type': './td[4]', 'protocol': ''}
        }
        if text is not None:
            return self._parser.parse(text, attr)

    def download(self):
        url = 'http://www.66ip.cn/2.html'
        r = requests.get(url=url, headers=HEADER, timeout=5)
        if (not r.ok) or len(r.content) < 500:
            raise ConnectionError
        else:
            return r.text


class Parser(object):
    def __init__(self):
        pass

    def parse(self, text, attr):
        if attr['type'] == 'xpath':
            return self.xpath_parse(text, attr)
        else:
            return None

    def xpath_parse(self, text, attr):
        proxy_list = []
        root = etree.HTML(text)
        proxies = root.xpath(attr['pattern'])
        for proxy in proxies:
            ip = proxy.xpath(attr['position']['ip'])[0].text
            port = proxy.xpath(attr['position']['port'])[0].text
            type = 0
            protocol = 0
            addr = 0
            country = 0
            area = 0

            proxy = {
                'ip': ip, 'port': port, 'types': type, 'protocol': protocol, 'country': country, 'area': area,
                'speed': 100
            }

            proxy_list.append(proxy)
        return proxy_list


spider = Spider()
print(spider.crawl())
