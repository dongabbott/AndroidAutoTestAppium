#-*-coding:utf-8 -*-

import os
import sys
import ConfigParser
import subprocess
from Outlog import framelog


#获取测试对象文件
def run(file):
    command = "python %s" % file
    p = subprocess.Popen(command,
                     universal_newlines=True,
                     stdout=subprocess.PIPE,
                     stdin=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     shell=True,)
    log = p.stdout.readlines()
    for line in log:
        framelog().info(line.strip())

#运行测试目录
def run_suite(suiteName):
    if os.path.exists(suiteName):
        fileAll = os.listdir(suiteName)
        for file in fileAll:
            if file.split('.')[-1] == 'py':
                filepath = "%s\\%s" % (suiteName, file)
                run(filepath)
    else:
        raise(NameError, u'目录不存在')

def run_all():
    try:
        cf = ConfigParser.ConfigParser()
        cf.read("./config/setting.ini")
    except IOError, err:
        print err
    suiteAll = cf.get('Project', 'casesuite').split(',')
    for suite in suiteAll:
        run_suite(suite)


if __name__ == "__main__":
    arg = sys.argv
    if len(arg) == 2:
        run_suite(arg[1])
    elif len(arg) == 1:
        run_all()
    else:
        raise(ArithmeticError, u'最多只支持一个参数')
