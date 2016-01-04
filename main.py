# -*- coding: utf-8 -*-

import os
import time
import shutil
import config
import logging
from receiver import Receiver

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
    re = Receiver()
    re.connect()
    re.run()