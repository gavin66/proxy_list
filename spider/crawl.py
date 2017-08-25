# -*- coding: UTF-8 -*-
class Crawl(object):
    def _transparent(self):
        raise NotImplementedError

    def _anonymous(self):
        raise NotImplementedError

    def _text(self, url):
        raise NotImplementedError

    def _parse(self, text):
        raise NotImplementedError

    def generator(self):
        raise NotImplementedError
