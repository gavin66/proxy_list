# -*- coding: UTF-8 -*-
import requests
import config
import json


class Crawl(object):
    def _transparent(self, page=1):
        raise NotImplementedError

    def _anonymous(self, page=1):
        raise NotImplementedError

    def _http(self):
        raise NotImplementedError

    def _https(self):
        raise NotImplementedError

    # @staticmethod
    @config.catch_exception_logging(None)
    def __proxy(self):
        """
        获取一个已爬代理
        :return:
        """
        response = requests.get('http://%s:%s/proxy?count=1' % (config.WEB_API_IP, config.WEB_API_PORT),
                                **{'timeout': 5})

        text = response.text
        proxy = json.loads(text)

        proxy = proxy[0]

        return {'ip': proxy[0], 'port': proxy[1]}

    @config.catch_exception_logging(None)
    def __proxy_delete(self, ip, port):
        """
        删除一个已爬代理
        :param ip:
        :param port:
        :return:
        """
        response = requests.get(
            'http://{}:{}/proxy/delete?ip={}&port={}'.format(config.WEB_API_IP, config.WEB_API_PORT, ip, port),
            **{'timeout': 5})

        if response.status_code == 204:
            config.console_log('删除代理成功 %s:%s' % (ip, port), 'green')
        else:
            config.console_log('删除代理失败 %s:%s' % (ip, port), 'red')

    @config.catch_exception_logging(None)
    def __request(self, proxy, url):
        """
        使用代理请求 url
        :param proxy:
        :param url:
        :return:
        """
        # 请求设置
        kwargs = {
            'timeout': 10,
            'headers': config.get_http_header()
        }

        # 有代理使用
        if isinstance(proxy, dict) and proxy:
            kwargs['proxies'] = {
                'http': 'http://%s:%s' % (proxy['ip'], proxy['port']),
                'https': 'http://%s:%s' % (proxy['ip'], proxy['port'])
            }

        response = requests.get(url, **kwargs)
        if response.ok and response.status_code == 200:
            return response.text
        else:
            config.console_log('请求返回的状态码: %s URL: %s 内容: %s' % (url, str(response.status_code), response.text),
                               'red')
            return None

    def _text(self, url):

        # 获取一个代理
        proxy = self.__proxy()

        # 已设置使用代理且已有代理
        if config.REQUEST_PROXY_RETRY and proxy:
            text = self.__request(proxy, url)

            # 代理已重试次数
            retried = 0
            # 总尝试次数
            try_total = 0
            while text is None:
                retried += 1
                try_total += 1
                # 重试次数已达限制,删除当前代理重获代理请求
                if retried > config.REQUEST_PROXY_RETRY:
                    self.__proxy_delete(proxy['ip'], proxy['port'])
                    proxy = self.__proxy()
                    # 清空代理重试次数
                    retried = 0
                text = self.__request(proxy, url)
                config.console_log('使用代理请求页面 %s ,总尝试第 %s 次' % (url, try_total), 'white')
        else:
            text = self.__request(None, url)

        return text

    def _parse(self, text):
        raise NotImplementedError

    def generator(self, page):
        for proxy in self._transparent(page):
            yield proxy
        for proxy in self._anonymous(page):
            yield proxy
