#-*-coding:utf-8 -*-

from appiumautolog import framelog
import random

class _DataValue(object):
    LETTERS = 'abcdefghigklmnopqrstuvwxyz'
    LETTERSBIG = 'ABCDEFGHIGKLMNOPQRSTUVWXYZ'
    NUMBER = '0123456789'
    SYMBOL = '!@#$%^&*()_-{}[]\\/"><.?,`~=+|\''


class DataDriver(_DataValue):
    """
    :arg
        -leng- length of need create str
    """
    def __init__(self):
        _DataValue.__init__(self)

    def createStrEN(self, length):
        strS = ''.join(random.sample(self.LETTERS+self.NUMBER+self.LETTERSBIG, length))
        return strS

    def createEmail(self, length, suffix="163.com"):
        email_name = random.sample(self.LETTERS+self.NUMBER, length)
        email = ''.join(email_name) + "@" + suffix
        framelog().debug(u'create Email 【%s】' % email)
        return email

    def createPassword(self,length):
        password = ''.join(random.sample(self.LETTERS+self.NUMBER+self.LETTERSBIG, length))
        framelog().debug(u'create password 【%s】' % password)
        return password