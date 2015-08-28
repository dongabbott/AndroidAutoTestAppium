#-*-coding:utf-8 -*-
import ConfigParser
import os
from Outlog import framelog
from HtmlTestRunner import HTMLTestRunner
import unittest
import time
import shutil
from reportDB import reportDB

# 获取路径下所有的测试类


def getClass(path):
    site = []
    if os.path.exists(path):
        fileAll = os.listdir(path)
        for f in fileAll:
            py_name = f.split('.')
            if py_name[-1] == 'py':
                site.append(py_name[0])
    else:
        framelog().error(u"测试目录不存在，请检查测试目录配置")
    if len(site) == 0:
        framelog().warning(u"测试目录没有可执行的测试文件")
    else:
        return site


# 运行目录下的case
def runCase(caseSuites):
    if isinstance(caseSuites, list):
        [__import__(str) for str in caseSuites]
        testSuite = unittest.TestSuite()
        suites = [unittest.TestLoader().loadTestsFromName(str)
                  for str in caseSuites]
        [testSuite.addTest(suite) for suite in suites]
        report_file = os.path.join(
            os.getcwd() + "\\tr\\tmp\\%s.html" % time.strftime("%Y_%m_%d_%H_%M_%S"))
        fp = file(report_file, 'wb')
        runner = HTMLTestRunner(
            stream=fp, title=u'测试报告', description=u'一路乐旅游自动化测试报告详细信息')
        result = runner.run(testSuite)
        fp.close()
        if result:
            index_file = os.path.join(os.getcwd() + "\\tr\\index.html")
            shutil.copy(report_file, index_file)
        allError = result.errors
        errorCase = [error[0].id() for error in allError]
        strError = ','.join(errorCase)
        AllFailures = result.failures
        failuresCase = [failures[0].id() for failures in AllFailures]
        strFailures = ','.join(failuresCase)
        errorCount = result.error_count
        rightCount = result.success_count
        failuresCount = result.failure_count
        caseCount = len(result.result)
        startTime = runner.startTime
        stopTime = runner.stopTime
        runTime = stopTime - startTime
        sql_count = "insert into run_result_count " \
            "values(null,'%s',%d,%d,%d,%d,'%s','%s','%s','%s',datetime('now', '+8 hour'))"\
            % (runTime,
               caseCount,
               errorCount,
               rightCount,
               failuresCount,
               strError,
               strFailures,
               startTime,
               stopTime)
        rid = reportDB().insertSql(sql_count)
        for resultOne in result.result:
            caseList = resultOne[1].id().split('.')
            caseClass = '.'.join(caseList[-2:])
            caseName = caseList[-1]
            caseStatus = resultOne[0]
            caseErrorInfo = resultOne[-1].replace("'", '"')
            sql_detail =  "insert into case_run_detail " \
                          "values(null,'%s','%s',%d,'%s',%d,datetime('now','+8 hour'))"\
                          % (caseName,
                             caseClass,
                             caseStatus,
                             caseErrorInfo,
                             rid)
            reportDB().insertSql(sql_detail)
    else:
        raise(TypeError, u'arg is must list')


if __name__ == "__main__":
    try:
        cf = ConfigParser.ConfigParser()
        cf.read("./config/setting.ini")
    except IOError, err:
        print err
    suiteAll = cf.get('Project', 'casesuite').split(',')
    case = []
    for suite in suiteAll:
        suite_case = getClass(suite)
        case += suite_case
    runCase(case)
