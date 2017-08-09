# -*- coding: UTF-8 -*-
import requests
from config import get_http_header


class Crawl(object):
    def __init__(self):
        self._session = requests.session()
        self._session.headers.update(get_http_header())
        self._request_kwargs = {
            'timeout': 5
        }

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
