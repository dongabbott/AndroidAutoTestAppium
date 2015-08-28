#-*-coding:utf-8 -*-
__author__ = 'DongJe'

import time
import subprocess
import os
import ConfigParser
from andapp.appiumautolog import appiumautolog
from mdappium import AppLoad
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class UIHandle():
    def __init__(self):
        self.driver = AppLoad().startActivity()
    def passFirstLoad(self):
        try:
            main_elements = WebDriverWait(self.driver, 10).until(
                lambda driver: self.driver.find_element_by_id(
                    "com.topview.slidemenuframe:id/load_up"))
            if main_elements:
                x = self.driver.get_window_size()['width']
                y = self.driver.get_window_size()['height']
                x_zuobiao = float(x) / float(2)
                y_start = float(y) * 4 / float(5)
                y_stop = float(y) / float(5)
                for m in range(2):
                    self.driver.swipe(x_zuobiao, y_start, x_zuobiao, y_stop)
                    time.sleep(1)
                element = WebDriverWait(self.driver, 5).until(
                    lambda driver: self.driver.find_element_by_class_name(
                        "android.widget.ImageButton"))
                element.click()
        except TimeoutException, e:
            pass
        return self.driver




def WaitElement(webDriver, method, timeout = None):
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
        cf = ConfigParser.ConfigParser()
        cf.read(setFile)
    except IOError, e:
        framelog().error(u'stting file can not open %s' % e)
    setOutTime = cf.get('AppConfig', 'elementTimeout')
    try:
        if timeout == None:
            elements = WebDriverWait(webDriver, int(setOutTime)).until(method)
        else:
            elements = WebDriverWait(webDriver, timeout).until(method)
    except TimeoutException, e:
        framelog().error(u"Element Load TimeOut [%s] %s" %(method, e))
    return elements



def coverInstall(apkPath):
    """
    install app of cover the mobile already exists
    :param apkPath: apk path of need to install
    :return:
    """
    command = "adb install -r %s" % apkPath
    p = subprocess.Popen(command,
                         universal_newlines=True,
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True,)
    while True:
        if p.poll() == 0:
            break
        elif p.poll() == -1:
            framelog().error('exec adb shell 【%s】 the device not found or mobile can not be shell' % command)
            break
        else:
            time.sleep(0.5)
    rData = p.stdout.readlines()
    framelog().debug('exec adb shell 【%s】 return %s' % (command, rData))
    return rData