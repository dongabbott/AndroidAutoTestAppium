#-*-coding:utf-8 -*-
import os
import settings
from andapp.appiumautolog import appiumautolog



# 获取连接电脑的手机驱动编号
def devices():
    '''
    :return:成功连接手机的可用驱动编号
    '''
    devices_command = "adb devices"
    command_out = os.popen(devices_command).readlines()
    if len(command_out) >= 3:
        devices_all = command_out[1:-1]
        devices = []
        for device_info in devices_all:
            device = device_info.strip("\n").split("\t")
            if len(device) == 2:
                device_name = device[0]
                device_status = device[1].strip("\n")
                if device_status == "device":
                    devices.append(device_name)
                else:
                    appiumautolog().error(u"连接编号为%s的手机未获得与电脑连接的权限！" % device_name)
                    raise Exception(u"连接编号为%s的手机未获得与电脑连接的权限！" % device_name)
        return devices
    else:
        appiumautolog().error(u"系统中adb命令不能正常使用或手机未正常连接！")
        raise AttributeError(u"系统中adb命令不能正常使用或手机未正常连接！")


# 获取测试app相关的信息
class apkmess:

    '''
    apk_path: 测试app的路径
    '''

    def __init__(self, apk_path):
        self.apk_path = apk_path

    def _get_apk_info_all(self):
        if os.path.exists(self.apk_path):
            cmd_command = "aapt dump badging %s" % self.apk_path
            apk_info = os.popen(cmd_command)
            info_dict = {}
            for one_info in apk_info:
                info = one_info.split(": ")
                if len(info) == 2:
                    val_key = info[0]
                    val_value = info[1]
                    info_dict[val_key] = val_value
            return info_dict
        else:
            raise Exception(u"测试apk路径不存在！")

    def _get_package_info(self, lab):
        package_info = self._get_apk_info_all().get(lab)
        all_info = package_info.split(" ")
        dict_info = {}
        for one in all_info:
            the_info = one.split("=")
            if len(the_info) == 2:
                info_key = the_info[0]
                info_value = the_info[1]
                dict_info[info_key] = info_value
        return dict_info

    # 获取测试包的包名
    @property
    def package_name(self):
        '''
        :return:测试包的包名
        '''
        return self._get_package_info("package").get("name").strip("'")

    # 获取测试包的版本号
    @property
    def version_code(self):
        '''
        :return:测试包的版本号
        '''
        return self._get_package_info("package").get("versionCode").strip("'")

    # 获取测试包的版本名称
    @property
    def version_name(self):
        '''
        :return:试包的版本名称
        '''
        return self._get_package_info("package").get("versionName").strip("\n").strip("'")

    # 获取应用名称
    @property
    def application_label(self):
        '''
        :return:应用名称
        '''
        label_info = self._get_package_info("launchable-activity")
        return label_info.get("label").strip("'")

    # 获取app的入口activity
    @property
    def launchable_activity(self):
        '''
        :return:welcome activity
        '''
        activity_info = self._get_package_info("launchable-activity")
        return activity_info.get("name").strip("'")
