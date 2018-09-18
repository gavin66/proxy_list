# -*- coding: UTF-8 -*-
import requests
from requests.exceptions import Timeout
import config


class Crawl(object):
    def _transparent(self, page=1):
        raise NotImplementedError

    def _anonymous(self, page=1):
        raise NotImplementedError

    def _http(self):
        raise NotImplementedError

    def _https(self):
        raise NotImplementedError

    def _text(self, url):
        try:
            response = requests.get(url, **{'timeout': 10, 'headers': config.get_http_header()})
            if response.ok:
                return response.text
            else:
                # todo 使用代理重新尝试下载
                config.console_log('请求返回的状态码: ' + str(response.status_code), 'red')
                return None
        except Timeout as e:
            config.console_log('请求超时: ' + str(e), 'red')
            return None

    def _parse(self, text):
        raise NotImplementedError

    def generator(self, page):
        for proxy in self._transparent(page):
            yield proxy
        for proxy in self._anonymous(page):
            yield proxy
