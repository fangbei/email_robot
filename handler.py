# -*- coding: utf-8 -*-

import re
import time
import queue
import message
import logging
import handle.echo as echo

class Handler(object):
    def __init__(self):
        super(Handler, self).__init__()
        self._finished = False
        self._queue = queue.Queue()
        self._result_queue = queue.Queue()
        self._handler = {"echo" : echo.Echo()}

    def _fetch(self):
        try:
            return self._queue.get(block=False)
        except Exception as e:
            return None

    def _unpack(self, pack):
        assert(isinstance(pack, str))
        if (isinstance(pack, str)):
            r = re.match("^(\w+)\s*:\s*((\w|\n)+)$", pack)
            if r != None:
                return r.group(1), r.group(2)
        return None, None

    def _handle(self, msglist):
        for msg in msglist:
            code, struct = self._unpack(msg.content())
            if code != None and struct != None:
                handle = self._handler.get(code)
                if handle != None:
                    result = handle.handler(struct)
                    if result != None:
                        self._result_queue.put(message.Message(msg.address(), result))
                else:
                    self._result_queue.put(message.Message(msg.address(), u"无法识别的命令"))
            else:
                self._result_queue.put(message.Message(msg.address(), u"非法的命令格式"))

    def push(self, msg):
        assert(isinstance(msg, message.Message))
        if isinstance(msg, message.Message):
            self._queue.put(msg)

    def run(self):
        logging.info("start handle emails")
        while not self._finished:
            msglist = []
            msg = self._fetch()
            while msg != None:
                msglist.append(msg)
                msg = self._fetch()
            if len(msglist) > 0:
                self._handle(msglist)
            else:
                time.sleep(1)

    def stop(self):
        assert(self._finshed == False)
        self._finished = True
        logging.info("stop handle emails")