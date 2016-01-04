# -*- coding: utf-8 -*-

class Message(object):
    def __init__(self, address='', content=''):
        super(Message, self).__init__()
        assert(isinstance(address, str))
        assert(isinstance(content, str))
        if isinstance(address, str):
            self._address = address
        if isinstance(content, str):
            self._content = content

    def address(self):
        return self._address

    def content(self):
        return self._content

    def setAddress(self, address):
        assert(isinstance(address, str))
        if isinstance(address, str):
            self._address = address

    def setContent(self, content):
        assert(isinstance(content, str))
        if isinstance(content, str):
            self._content = content