# -*- coding: utf-8 -*-

import time
import const
import email
import queue
import imaplib
import message
import logging

class Receiver(object):
    def __init__(self):
        super(Receiver, self).__init__()
        self._finshed = False
        self._imap_hanlde = None
        self._queue = queue.Queue()

    def _receive(self):
        assert(self._imap_hanlde != None and not self._finshed)
        if self._imap_hanlde != None and not self._finshed:
            from_address = content = None
            self._imap_hanlde.select("INBOX")
            status, data = self._imap_hanlde.search(None, "UNSEEN")
            for num in data[0].split():
                status, data = self._imap_hanlde.fetch(num, "(RFC822)")
                email_message = email.message_from_bytes(data[0][1])
                if email_message != None:
                    from_address = email.utils.parseaddr(email_message.get("from"))[1]
                    for part in email_message.walk():
                        if not part.is_multipart():
                            if not part.get_param("name") and part.get_content_type() == "text/plain":
                                charset = part.get_content_charset()
                                if charset:
                                    content = part.get_payload(decode=True).decode(charset)
                                else:
                                    content = part.get_payload(decode=True).decode()
                    self._imap_hanlde.store(num, '+FLAGS', '\\Seen')
                if from_address != None and content != None:
                    self._queue.put(message.Message(from_address, content))
                    logging.info("".join(("frome address:", from_address, " text:", content)))
                from_address = content = None
            time.sleep(5)

    def fetch(self):
        try:
            return self._queue.get(block=False)
        except Exception as e:
            return None

    def connect(self):
        assert(self._imap_hanlde == None)
        if self._imap_hanlde != None:
            return True
        try:
            logging.info("login IMAP server")
            if const.IMAP_SSL:
                self._imap_hanlde = imaplib.IMAP4_SSL(const.IMAP_ADDRESS, const.IMAP_PORT)
            else:
                self._imap_hanlde = imaplib.IMAP4(const.IMAP_ADDRESS, const.IMAP_POR)
            self._imap_hanlde.login(const.IMAP_USER_NAME, const.IMAP_PASSWORD)
            logging.info("login IMAP server success")
            return True
        except Exception as e:
            logging.error(e)
            self.close()
            return False

    def close(self):
        assert(self._imap_hanlde != None)
        if self._imap_hanlde != None:
            try:
                if self._imap_hanlde.state == "SELECTED":
                    self._imap_hanlde.close()
                self._imap_hanlde.logout()
                self._imap_hanlde = None
            except Exception as e:
                logging.error(e)
                pass

    def run(self):
        logging.info("start receive emails")
        while self._imap_hanlde != None and not self._finshed:
            try:
                self._receive()
            except Exception as e:
                logging.error(e)
                self.stop()
        self.close()

    def stop(self):
        assert(self._finshed == False)
        self._finshed = True
        logging.info("stop receive emails")