# -*-coding:utf-8
from urllib2 import URLError
from andapp.appiumautolog import appiumautolog
from tapp import apkmess
import tapp
from appium import webdriver
from mobilehard import mobilehard
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
import re
import settings
from ADBShell import AdbCommand

class SettingsConfException(Exception):
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

try:
    settings.APKPATH
    settings.APPIUMSERVER
    settings.ELEMENTTIMEOUT
except AttributeError, e:
    print e
    raise SettingsConfException(u"配置文件出错！")



class appload:
    def __init__(self, device):
        if isinstance(device, str):
            self.device = device
        else:
            raise ValueError(u'驱动编号必须是一个字符串！')
    def startapp(self, activity=apkmess(settings.APKPATH).launchable_activity):
        '''
        :param activityName: android activity name
        :return: driver
        '''
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = mobilehard(self.device).mobile_android_version
        desired_caps['deviceName'] = self.device
        app_info = apkmess(settings.APKPATH)
        desired_caps['appPackage'] = app_info.package_name
        desired_caps['appActivity'] = activity
        try:
            appiumautolog().debug(u'appium启动信息 %s' % desired_caps)
            self.driver = webdriver.Remote(settings.APPIUMSERVER, desired_caps)
        except URLError, e:
            appiumautolog().error(u'请检果appium服务器地址是否正确! \t %s ' % e)
        except WebDriverException, err:
            appiumautolog().error(u'appium服务器被占用!, \t %s' % err)
        return self.driver

    def coverinstall(self, apkpath = settings.APKPATH):
        '''
        :param apkpath: 需要被安装的app的路径，默认为配置文件路径
        :return:Ture or False
        '''
        ins_command = AdbCommand(self.device).shell.get("coverInd") + ' ' + apkpath
        run = mobilehard(self.device).execadbshell(ins_command)
        if run:
            result = [x for x in run if x!='\n'][1]
            if re.match(r"^Failure*", result):
                appiumautolog().error(u"此版本不能覆盖比自己高的版本！")
                return False
            elif re.match(r"^Success*", result):
                return True
            else:
                appiumautolog().error(u"adb命令运行有误！")
                raise Exception(u"adb命令运行有误！")
        else:
            appiumautolog().error(u"adb命令运行有误!")
            raise Exception(u"adb命令运行有误！")



def WaitElement(webDriver, method, timeout = settings.ELEMENTTIMEOUT):
    '''
    set find elements auto wait
    :param webDriver: the start webdriver
    :param method: the method of check page element
    :param timeout: Timeout
    :return: element
     Example:
            from appo.specialUi import WaitElement \n
            element = WaitElement(driver, lambda x: x.find_element_by_id("someId"), 10)
    '''
    try:
        elements = WebDriverWait(webDriver, timeout).until(method)
    except TimeoutException, e:
        appiumautolog().error(u"页面加载超时 [%s] %s" %(method, e))
    return elements
