#-*-coding:utf-8 -*-
import subprocess
from andapp.appiumautolog import appiumautolog
from ADBShell import AdbCommand
import time
import os
# get the phone Hardware info

class mobilehard():
    '''
        get hardware base device name
    '''
    def __init__(self, deviceName):
        '''
        :param : 驱动编号
        :return: the mobile connect pc device name
        '''
        self.deviceName = deviceName

    def execadbshell(self, shell):
        p = subprocess.Popen(shell,
                             universal_newlines=True,
                             stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             shell=True,)
        while True:
            if p.poll() == 0:
                break
            elif p.poll() == -1:
                appiumautolog.error('执行adb命令[%s],系统中adb环境存在问题！' % shell)
                break
            else:
                time.sleep(0.5)
        rData = p.stdout.readlines()
        appiumautolog().debug('执行adb命令[%s],返回结果 %s' % (shell, rData))
        return rData



    def _cpu_info(self):
        command = AdbCommand(self.deviceName).shell.get("getCpu")
        cpuinfo = self.execadbshell(command)
        return cpuinfo

    # get mobile cpu version
    @property
    def mobile_cpu_info(self):
        '''
        :return:cpu name
        '''
        for line in self._cpu_info():
            if line.strip() != "":
                lineinfo = line.split(":")
                if str(lineinfo[0]).strip() == "Hardware":
                    cpuversion = str(lineinfo[1]).strip()
        return cpuversion

    # get mobile cpu thread number
    @property
    def mobile_cpu_thread(self):
        '''
        :return:cpu core number
        '''
        number = 0
        for line in self._cpu_info():
            if line.strip() != "":
                process = str(line.split(":")[0]).strip()
                if process == "processor":
                    number += 1
        return number

    # get mobile memory all info
    def _mem_info(self):
        command = AdbCommand(self.deviceName).shell.get("getMem")
        meminfo = self.execadbshell(command)
        return meminfo

    # get mobile memory size
    @property
    def mobile_mem_size(self):
        '''
        :return:memory size
        '''
        mem_total = self._mem_info()[0]
        mem_size = mem_total.split(":")[-1].strip().split(" ")[0]
        size_to_mb = float(mem_size)/float(1024*1024)
        if size_to_mb >= 1:
            size = round(size_to_mb,0)
            return str("%s GB" %size)
        else:
            if size_to_mb>0.5:
                return str("1 GB")
            else:
                return str("512 MB")



    def _mobile_info_list(self):
        command = AdbCommand(self.deviceName).shell.get("GetProp")
        getPropData = os.popen(command).readlines()
        dictinfo = {}
        for thisone in getPropData:
            try:
                infokey = str(thisone.split(":")[0]).strip().strip(
                    "[").strip("]")
                infovalue = str(thisone.split(":")[1]).strip().strip(
                    "[").strip("]")
                dictinfo[infokey] = infovalue
            except Exception, e:
                pass
        return dictinfo

    # get the mobile name where connect the computer
    @property
    def get_mobile_name(self):
        return self._mobile_info_list().get("ro.product.device")

    # get the android version in the mobile connect the computer
    @property
    def mobile_android_version(self):
        return self._mobile_info_list().get("ro.build.version.release")

    # get mobile network info ip address
    @property
    def mobile_ip(self):
        return self._mobile_info_list().get("dhcp.wlan0.ipaddress")

    # get mobile network info geteway
    @property
    def mobile_geteway(self):
        return self._mobile_info_list().get("dhcp.wlan0.gateway")

    # get mobile network info DNS
    @property
    def mobile_dns(self):
        dns = []
        for dnskeys in self._mobile_info_list().keys():
            if "dhcp.wlan0.dns" in dnskeys:
                wl = self._mobile_info_list().get(dnskeys)
                if wl != "":
                    dns.append(wl)
        return dns

    # get mobile screen size
    @property
    def mobile_resolution(self):
        size = self._mobile_info_list().get("persist.sys.screen.size")
        size_x = self._mobile_info_list().get("persist.sys.default.res.xres")
        size_y = self._mobile_info_list().get("persist.sys.default.res.yres")
        if size == None:
            screen = str(size_x) + "*" + str(size_y)
        else:
            screen = size
        return screen
