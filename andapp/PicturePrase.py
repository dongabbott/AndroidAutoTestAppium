#-*-coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import ConfigParser
from reportDB import reportDB

class GetDatabase(object):
    #获取最新的5次测试统计数据
    try:
        cf = ConfigParser.ConfigParser()
        cf.read("E:\\apk\\huodong\\config\\setting.ini")
    except IOError, err:
        print err
    count = cf.get('Graph', 'count')
    LATE_FIVE_SQL = 'select errorCount,rightCount,failCount,startTime ' \
                    'from run_result_count ' \
                    'ORDER BY id DESC ' \
                    'LIMIT %s;' %int(count)

    #获取历史的成功与失败条数
    ALL_PASS_FAILED = "select errorCount+failCount,rightCount from run_result_count"


class CreateGraph(GetDatabase):
    def __init__(self):
        GetDatabase.__init__(self)
    #生成柱状图
    def bargraph(self):
        ind = np.arange(int(self.count))
        width = 0.25
        data = reportDB().selectSql(self.LATE_FIVE_SQL)
        errorsList = tuple(error[0] for error in data)[::-1]
        passedList = tuple(right[1] for right in data)[::-1]
        failedList = tuple(fail[2] for fail in data)[::-1]
        startTime = tuple(runtime[3] for runtime in data)[::-1]
        fig, ax = plt.subplots()
        ax.set_ylabel(u'个数')
        ax.set_title(u'最近%s次测试结果柱状图' % self.count)
        ax.set_xticks(ind+width)
        ax.set_xticklabels(startTime,rotation=18, fontsize='small')
        rectError = ax.bar(ind, errorsList, width, color='r')
        rectFail = ax.bar(ind+width, failedList, width, color='y')
        rectPass = ax.bar(ind+2*width, passedList, width, color='g')
        fontP = FontProperties()
        fontP.set_size('small')
        for e_rect in rectError:
            height = e_rect.get_height()
            ax.text(e_rect.get_x()+e_rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')
        for f_rect in rectFail:
            height = f_rect.get_height()
            ax.text(f_rect.get_x()+f_rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')
        for p_rect in rectPass:
            height = p_rect.get_height()
            ax.text(p_rect.get_x()+p_rect.get_width()/2., 0.8*height, '%d'%int(height),
                    ha='center', va='bottom')
        ax.legend( (rectError[0], rectPass[0], rectFail[0]), (u'错误', u'通过', u'失败'),prop = fontP)
        plt.savefig('E:\\apk\huodong\\tr\\pic\\bargraph')

    #生成全部结果线性图
    def linegraph(self):
        data = reportDB().selectSql(self.ALL_PASS_FAILED)
        errors = tuple(error[0] for error in data)
        rights = tuple(right[1] for right in data)
        plt.ylabel(u'个数')
        plt.title(u'测试结果线性图')
        plt.plot(errors,color='r')
        plt.plot(rights, color='g')
        plt.savefig('E:\\apk\huodong\\tr\\pic\\linegraph')

    def linegraph(self):
        data = reportDB().selectSql(self.ALL_PASS_FAILED)
        errors = tuple(error[0] for error in data)
        rights = tuple(right[1] for right in data)
        plt.ylabel(u'个数')
        plt.title(u'测试结果线性图')
        plt.plot(errors,color='r')
        plt.plot(rights, color='g')
        plt.savefig('E:\\apk\huodong\\tr\\pic\\linegraph')


a = CreateGraph().linegraph()
b = CreateGraph().bargraph()