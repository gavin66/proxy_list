# -*- coding: UTF-8 -*-
class Base(object):
    def list(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

    def add(self, data):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def handler(self):
        raise NotImplementedError
