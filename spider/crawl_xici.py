# -*- coding: UTF-8 -*-
from spider.crawl import Crawl
from lxml import etree
from config import catch_exception_logging


class XiCi(Crawl):
    """
    http://www.xicidaili.com/
    """

    def _transparent(self, page=1):
        """
        获取透明代理

        :param page: 页数，默认第一页
        :rtype: list 返回此页的代理列表
        """
        url = 'http://www.xicidaili.com/nt/%u' % page
        return self._parse(self._text(url))

    def _anonymous(self, page=1):
        """
        获取匿名代理

        :param page: 页数，默认第一页
        :rtype: list 返回此页的代理列表
        """
        url = 'http://www.xicidaili.com/nn/%u' % page
        return self._parse(self._text(url))

    @catch_exception_logging(list())
    def _parse(self, text):
        proxies = list()
        root = etree.HTML(text)
        ip_list = root.xpath(".//*[@id='ip_list']/tr[position()>1]")

        if not ip_list:
            return list()

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
