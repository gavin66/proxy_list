# -*- coding: UTF-8 -*-
class Base(object):
    def list(self):
        raise NotImplementedError

    def add(self, data):
        raise NotImplementedError

    def update(self, data):
        raise NotImplementedError

    def delete(self, data):
        raise NotImplementedError

    def handler(self):
        raise NotImplementedError
