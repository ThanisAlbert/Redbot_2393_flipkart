import inspect
import logging
from datetime import datetime


class Log:

    def __init__(self,a,b):
        self.a= a
        self.b=b

    def getLogger(self):
        logger = logging.getLogger('sgd_svrg')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s : %(message)s : %(asctime)s')
        fh = logging.FileHandler("Log.log")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger