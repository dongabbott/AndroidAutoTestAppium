#-*-coding:utf-8 -*-
from andapp.appo.mdappium import appload, WaitElement
from andapp.appo.tapp import devices
import unittest
from ddt import unpack, data, ddt
import time


@ddt
class account_user_login(unittest.TestCase):

    def setUp(self):
        device = devices()
        self.driver = appload(device[0]).startapp()
        main =WaitElement(self.driver, lambda driver: self.driver.find_element_by_id('com.topview.slidemenuframe:id/tv_homepage_bottom_person'))
        main.click()
        self.driver.find_element_by_id('com.topview.slidemenuframe:id/ll_user_info').click()

    def tearDown(self):
        self.driver.quit()

    @data(
        ('13476085026', '123456'),#手机号登录
        ('dongjie', '123456'),#平台帐号登录
        ('690455420@qq.com','123456'),#邮箱
    )
    @unpack
    def test_input_login(self, username, pwd):
        user_input = self.driver.find_element_by_id('com.topview.slidemenuframe:id/user_name')
        user_input.send_keys(username)
        pwd_input = self.driver.find_element_by_id('com.topview.slidemenuframe:id/user_pwd')
        pwd_input.send_keys(pwd)
        self.driver.find_element_by_id('com.topview.slidemenuframe:id/user_login').click()
        user_ico = self.driver.find_element_by_id('com.topview.slidemenuframe:id/tv_integration')
        self.assertIsNotNone(user_ico)
        user_ico.click()
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        jd_x = float(x) / float(2)
        y_start = float(y) * 4 / float(5)
        user_x_stop = float(y) / float(5)
        for x in range(2):
            self.driver.swipe(jd_x, y_start, jd_x, user_x_stop)
            time.sleep(1)
        self.driver.find_element_by_id('com.topview.slidemenuframe:id/btn_logout').click()
        self.driver.find_element_by_id('android:id/button1').click()



    @data(
        (),#手机号登录
        (),#平台帐号登录
        (),#邮箱
    )
    @unpack

    def test_third_login(self, login_element):
        pass

