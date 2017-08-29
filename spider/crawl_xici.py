# -*- coding: UTF-8 -*-
import config
from spider.crawl import Crawl
from lxml import etree
import requests
import time


class XiCi(Crawl):
    def transparent(self, page=1):
        """
        获取透明代理

        :param page: 页数，默认第一页
        :rtype: list 返回此页的代理列表
        """
        url = 'http://www.xicidaili.com/nt/%u' % page
        return self._parse(self._text(url))

    def anonymous(self, page=1):
        """
        获取匿名代理

        :param page: 页数，默认第一页
        :rtype: list 返回此页的代理列表
        """
        url = 'http://www.xicidaili.com/nn/%u' % page
        return self._parse(self._text(url))

    def _text(self, url):
        response = requests.get(url, **{'timeout': 5, 'headers': config.get_http_header()})
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

    def generator(self):
        page = 1
        while page < 11:
            for proxy in self.transparent(page):
                yield proxy
            for proxy in self.anonymous(page):
                yield proxy
            # 爬取下一页
            page += 1
            # 如果到 10 页，重新再从第 1 页开始并睡眠15分钟，一直循环下去
            if page == 11:
                page = 1
                time.sleep(60 * 15)
