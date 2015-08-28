#-*-coding:utf-8 -*-
__author__ = 'DongDie'
#mobile adb command

class AdbCommand(object):
    def __init__(self, deviceNname):
        self.deviceNname = deviceNname
        self.shell = {
            #get the all devices name there mobile connect the computer
            'AllDevices':'adb devices',
            #get detailed information of the designated mobile phone
            'GetProp': 'adb -s %s shell getprop' % self.deviceNname,
            #get detailed cpu info of the designated mobile phone
            'getCpu' : 'adb -s %s shell cat /proc/cpuinfo' % self.deviceNname,
            #get detailed memory info of the designated mobile phone
            'getMem' : 'adb -s %s shell cat /proc/meminfo' % self.deviceNname,
            #install apk cover the old
            'coverInd' : 'adb -s %s install -r' % self.deviceNname,
        }