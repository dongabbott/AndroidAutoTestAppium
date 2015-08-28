#-*-coding:utf-8 -*-


#创建测试结果存储数据库
#结果表:run_result_count
#|id      |runtime    |caseCount    |errorCount   |rightCount    |failCount     |errorCase     |failCase    |startTime    |stopTime     |createdTime   |
#|ID自增  |运行时间    |用例总数     |错误case数量 |成功case数量   |失败的case数量 |错误case       |失败case   |开始时间     |结束时间       |创建时间      |

#详细结果表:case_run_detail
#|id      |caseName   |className    |status         |runInfo      |rid         |createdTime   |
#|ID自增  |用例名      |所属类名     |0,通过;1,失败   |错误信息     |运行时的id   |创建时间      |

import sqlite3
from appiumautolog import framelog

class CreateDB(object):
    #数据库存放路径
    DB_FILE = "E:\\apk\\huodong\\tr\\DB\\resultDb"
    #创建统计表
    CREATE_COUNT_SQL = "create table if not exists run_result_count" \
                       "(id integer primary key autoincrement," \
                       "runtime TEXT," \
                       "caseCount integer," \
                       "errorCount integer," \
                       "rightCount integer," \
                       "failCount integer,"\
                       "errorCase varchar(3000)," \
                       "failCase varchar(3000)," \
                       "startTime TEXT," \
                       "stopTime  TEXT," \
                       "createdTime TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP)"
    #创建用例详细表
    CREATE_DETAIL_SQL = "create table if not exists case_run_detail" \
                        "(id integer primary key autoincrement," \
                        "caseName varchar(50)," \
                        "className integer," \
                        "status integer," \
                        "runInfo varchar(3000)," \
                        "rid integer, " \
                        "CreatedTime TimeStamp NOT NULL DEFAULT CURRENT_TIMESTAMP)"



class reportDB(CreateDB):
    def __init__(self):
        CreateDB.__init__(self)
    def _createDatabase(self):
        try:
            conn = sqlite3.connect(self.DB_FILE)
            conn.cursor()
            conn.execute(self.CREATE_COUNT_SQL)
            conn.execute(self.CREATE_DETAIL_SQL)
            conn.commit()
            return conn
        except Exception, e:
            framelog().error(e)

    def insertSql(self, sql):
        connect = self._createDatabase()
        framelog().debug("执行SQLite语句 %s" %sql)
        try:
            inId = connect.execute(sql)
            connect.commit()
            connect.close()
            return inId.lastrowid
        except Exception, e:
            framelog().error(e)

    def selectSql(self, sql):
        connect = self._createDatabase()
        framelog().debug("执行SQLite语句 %s" %sql)
        try:
            action = connect.execute(sql)
            connect.commit()
            if action:
                re = action.fetchall()
            else:
                framelog().warning("执行语句没有结果返回")
            connect.close()
            return re
        except Exception, e:
            framelog().error(e)