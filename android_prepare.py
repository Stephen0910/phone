#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2017/4/1 14:45
# @Author   : zhangjian
# @Site     : 
# @File     : new_frame.py
# @Purpose  :
# @Software : PyCharm Community Edition
# @Copyright:   (c) zhangjian 2017
# @Licence  :     <your licence>
"""
逍遥模拟器端口：adb connect 127.0.0.1:21503
夜游神模拟器端口：adb connect 127.0.0.1:52001
adb shell /system/bin/screencap -p /sdcard/screenshot.png（保存到SDCard）
adb pull /sdcard/screenshot.png d:/screenshot.png（保存到电脑）
"""
import logging
import os
import time

import atx

# 设置游戏包名，图片保存目录
package = ""
image_file = "Slot"

# 判断是否存在imagefile的文件夹，没有则创建，用于存放日志和截图等
cur_dir = os.getcwd()
if os.path.exists(cur_dir + "\\" + image_file):
    print "yes"
else:
    os.mkdir(image_file)


def devices_connect():
    """
    返回所有连接设备的序列号，设备连接adb，注意打开开发者选项，USB调试，授权
    :return: 序列号列表
    """
    devices = os.popen("adb devices").readlines()
    device_list = []
    for device_no in devices:
        if "List" not in device_no and len(device_no) != 1:
            # print "device_no", device_no
            device_list.append(device_no.split()[0])
    return device_list


def write_log(log_string):
    """
    写log文件到image_file
    :param log_string:输入的log信息
    :return:
    """
    curtime = time.strftime("%Y-%m-%d %X", time.localtime())
    # print curtime
    cur_dir = os.getcwd()
    print "cur_dir = ", cur_dir
    log_path = cur_dir + "\\" + image_file + "\log.txt"
    print "log_path = ", log_path
    # with open(u'log.txt', 'a') as f:
    with open(log_path, 'a') as f:
        f.write(str(curtime) + " " * 5 + log_string + '\n')


def relative_name(image_name):
    """
    重定义图片，输入为名字，变成相对路径图片
    :param image_name: 图片名字
    :return:
    """
    file_dir = os.getcwd() + "\%s" % image_file
    return file_dir + "\%s" % image_name


def screen_shot():
    """
    截屏手机屏幕到当前目录的下一层目录，默认为转屏后的
    :return:
    """
    path = os.getcwd()
    print path

    picture_name = int(time.time())
    print picture_name

    os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.png")
    os.system("adb pull /sdcard/screenshot.png %s/%s.png" % (path + "/" + image_file, picture_name))


if __name__ == '__main__':
    pass
