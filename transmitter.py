# -*- coding: utf-8 -*-

import time
import queue
import email
import const
import config
import smtplib
import logging

class Transmitter(object):
    def __init__(self):
        self._finished = False
        self._queue = queue.Queue()
        super(Transmitter, self).__init__()

    def fetch(self):
        try:
            return self._queue.get(block=False)
        except Exception as e:
            return None

    def _send(self, msglist):
        pass

    def run(self):
        logging.info("start sending emails")
        while not self._finished:
            msglist = []
            msg = self.fetch()
            while msg != None:
                msglist.append(msg)
                msg = self.fetch()
            if len(msglist) > 0:
                self._send(msglist)
            else:
                time.sleep(1)

    def stop(self):
        assert(self._finshed == False)
        self._finished = True
        logging.info("stop sending emails")