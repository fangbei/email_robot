# -*- coding: utf-8 -*-

import time
import queue
import message
import logging
import handler.echo as echo

class Handler(object):
    def __init__(self):
        super(Handler, self).__init__()
        self._finished = False
        self._queue = queue.Queue()
        self._handler = {"echo" : echo.Echo()}

    def _fetch(self):
        try:
            return self._queue.get(block=False)
        except Exception as e:
            return None

    def _handle(self, msglist):
        pass

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