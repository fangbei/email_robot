# -*- coding: utf-8 -*-

import time
import queue
import email
import const
import smtplib
import message
import logging
from email.header import Header
from email.mime.text import MIMEText

class Transmitter(object):
    def __init__(self):
        super(Transmitter, self).__init__()
        self._finished = False
        self._queue = queue.Queue()

    def _connect(self):
        count = 0
        smtp_hanlde = None
        logging.info("login SMTP server")
        while count < 3:
            try:
                smtp_hanlde = smtplib.SMTP(const.SMTP_ADDRESS, const.SMTP_PORT)
                if const.SMTP_TLS:
                    smtp_hanlde.starttls()
                smtp_hanlde.login(const.SMTP_USER_NAME, const.SMTP_PASSWORD)
                logging.info("login SMTP server success")
                break
            except Exception as e:
                logging.warning(e)
                count += 1
                logging.info("try again to login SMTP server. {0}".format(count))
        return smtp_hanlde

    def _send(self, msglist):
        smtp_hanlde = self._connect()
        if smtp_hanlde == None:
            self.stop()
        else:
            for msg in msglist:
                from_address = "{0} <{1}>".format(Header(u"Robot",'utf-8'), const.SMTP_USER_NAME)
                message = MIMEText(msg.content(), 'plain', 'utf-8')
                message["From"] = from_address
                message["To"] = msg.address()
                message["Subject"] = u"来自邮箱机器人的回信"
                message["Date"] = email.utils.formatdate()
                message["Accept-Language"] = "zh-CN"
                message["Accept-Charset"] = "ISO-8859-1,utf-8"
                message["Message-ID"] = email.utils.make_msgid()
                try:
                    smtp_hanlde.sendmail(const.SMTP_USER_NAME, msg.address(), message.as_string())
                    logging.info("send success")
                except Exception as e:
                    logging.error(e)
            smtp_hanlde.close()

    def _fetch(self):
        try:
            return self._queue.get(block=False)
        except Exception as e:
            return None

    def push(self, msg):
        assert(isinstance(msg, message.Message))
        if isinstance(msg, message.Message):
            self._queue.put(msg)

    def run(self):
        logging.info("start send emails")
        while not self._finished:
            msglist = []
            msg = self._fetch()
            while msg != None:
                msglist.append(msg)
                msg = self._fetch()
            if len(msglist) > 0:
                self._send(msglist)
            else:
                time.sleep(1)

    def stop(self):
        assert(self._finshed == False)
        self._finished = True
        logging.info("stop send emails")