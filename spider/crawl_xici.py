# -*- coding: UTF-8 -*-
from spider.crawl import Crawl
from lxml import etree


class XiCi(Crawl):
    def __init__(self):
        Crawl.__init__(self)

    def _transparent(self):
        pass

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
                        proxy['anonymity'] = 'anonymous'
                        print(proxy)
                    page += 1
                else:
                    fail += 1
            else:
                fail += 1
            # 如果失败大于5次,停止爬取
            if fail > 5:
                done = True

    def _http(self):
        pass

    def _https(self):
        pass

    def _text(self, url):
        r = self._session.get(url, **self._request_kwargs)
        if r.ok:
            return r.text
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
                'protocol': protocol,  # http https http/https
                'speed': 0.2
            }

            proxies.append(proxy)

        return proxies

    def generator(self, anonymity='http'):
        pass

    def test(self):
        # self._parse(self._content('http://www.xicidaili.com/nn/1'))
        self._anonymous()


if __name__ == '__main__':
    c = XiCi()
    c.test()
