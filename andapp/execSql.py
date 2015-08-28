#-*-coding:utf-8 -*-
# 连接数据库执行sql返回值
import pymssql
import MySQLdb
import ConfigParser
from appiumautolog import appiumautolog

class ExecSQL():
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    #执行SQLserver查询
    def exec_mssql(self, sql):
        try:
            conn = pymssql.connect(host = self.host,
                                   port = self.port,
                                   user = self.user,
                                   password = self.password,
                                   database = self.database,
                                   charset="utf8")
            cur = conn.cursor()
            if cur:
                appiumautolog().debug(u"执行SQL语句|%s|" %sql)
                cur.execute(sql)
                rows = cur.fetchall()
                if len(rows) == 0:
                    appiumautolog().warning(u"没有查询到数据")
                else:
                    appiumautolog().debug(u"返回执行结果%s" %rows)
                return rows
            else:
                appiumautolog().error(u"数据库连接不成功")
            conn.close()
        except Exception, e:
            appiumautolog().error(e)

    #执行Mysql查询
    def exec_mysql(self, sql):
        try:
            conn = MySQLdb.connect(self.host,
                                   self.port,
                                   self.user,
                                   self.password,
                                   self.database)
            cur = conn.cursor()
            if cur:
                appiumautolog().info(u"执行SQL语句|%s|" %sql)
                resList = cur.execute(sql)
                return resList
        except Exception, e:
            appiumautolog().error(e)


def ExecSqlServer(sql):
    try:
        cf = ConfigParser.ConfigParser()
        cf.read("E:\\apk\\huodong\\config\\setting.ini")
        host = cf.get("DataBase", "host")
        port = cf.get("DataBase", "port")
        user = cf.get("DataBase", "user")
        password = cf.get("DataBase", "password")
        database = cf.get("DataBase", "database")
        data = ExecSQL(host, port, user, password, database).exec_mssql(sql)
        return data
    except IOError, e:
        framelog().error(u"配置文件发生异常")

