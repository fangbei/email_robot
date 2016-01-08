# -*- coding: utf-8 -*-

import os
import time
import shutil
import config
import logging
import threading
from handler import Handler
from receiver import Receiver
from transmitter import Transmitter

def InitLogging():
    if os.path.exists("logs"):
        if os.path.isfile("logs"):
            os.remove("logs")
            os.mkdir("logs")
    else:
        os.mkdir("logs")
    filename = ''.join(("logs", os.path.sep, time.strftime("%Y%m%d%H%M%S"), ".txt"))
    if os.path.isdir(filename):
        shutil.rmtree(filename, True)
    logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename=filename,
                    filemode="w")
    console = logging.StreamHandler()
    console.setLevel(logging.NOTSET)
    formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

if __name__ == '__main__':
    InitLogging()
    handler = Handler()
    receiver = Receiver()
    transmitter = Transmitter()
    receiver.connect()

    td1 = threading.Thread(target=lambda : handler.run())
    td2 = threading.Thread(target=lambda : receiver.run())
    td3 = threading.Thread(target=lambda : transmitter.run())
    td1.start()
    td2.start()
    td3.start()

    # main loop
    while True:
        if handler.is_runing() and receiver.is_runing() and transmitter.is_runing():
            msg = receiver.fetch()
            while msg != None:
                handler.push(msg)
                msg = receiver.fetch()
            msg = handler.fetch_to_send()
            while msg != None:
                transmitter.push(msg)
                msg = handler.fetch_to_send()
        else:
            break

    handler.stop()
    receiver.stop()
    transmitter.stop()

    td1.join()
    td2.join()
    td3.join()