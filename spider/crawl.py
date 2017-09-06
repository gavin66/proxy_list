# -*- coding: UTF-8 -*-
class Crawl(object):
    def _transparent(self):
        raise NotImplementedError

    def _anonymous(self):
        raise NotImplementedError

    def _http(self):
        raise NotImplementedError

    def _https(self):
        raise NotImplementedError

    def _text(self, url):
        raise NotImplementedError

    def _parse(self, text):
        raise NotImplementedError

    def generator(self, page):
        raise NotImplementedError
