#-*-coding:utf-8 -*-

import logging
import settings
import datetime
import os

logLevel = {
   1 : logging.NOTSET,
   2 : logging.DEBUG,
   3 : logging.INFO,
   4 : logging.WARNING,
   5 : logging.ERROR,
   6 : logging.CRITICAL
}


loggers = {}

def  appiumautolog():
    global loggers
    level = logLevel[settings.LOGLEVEL]
    filename = datetime.datetime.now().strftime('%Y-%m-%d')+'.log'
    logFile =  os.path.join(settings.LOGPATH, filename)
    logger = logging.getLogger()
    logger.setLevel(level)
    if not logger.handlers:
        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(logFile)
        fh.setLevel(level)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)
        loggers.update(dict(name=logger))
    return logger