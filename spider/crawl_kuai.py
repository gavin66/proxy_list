# -*- coding: UTF-8 -*-
from spider.crawl import Crawl
from lxml import etree
from config import catch_exception_logging


class Kuai(Crawl):
    """
    https://www.kuaidaili.com/
    """

    def _transparent(self, page=1):
        """
        获取透明代理

        :param page: 页数，默认第一页
        :rtype: list 返回此页的代理列表
        """
        url = 'https://www.kuaidaili.com/free/intr/%d/' % page
        return self._parse(self._text(url))

    def _anonymous(self, page=1):
        """
        获取匿名代理

        :param page: 页数，默认第一页
        :rtype: list 返回此页的代理列表
        """
        url = 'https://www.kuaidaili.com/free/inha/%d/' % page
        return self._parse(self._text(url))

    @catch_exception_logging
    def _parse(self, text):

        if text is None:
            return list()

        proxies = list()
        root = etree.HTML(text)
        ip_list = root.xpath(".//*[@id='list']/table[position()=1]/tbody/tr")

        if not ip_list:
            return None

        for item in ip_list:
            ip = item.xpath('./td[1]')[0].text
            port = item.xpath('./td[2]')[0].text

            # 国家
            country = ''

            # 地址
            try:
                address = item.xpath('./td[5]/a')[0].text
            except IndexError:
                address = ''

            # 协议
            protocol = item.xpath('./td[4]')[0].text.lower()

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
