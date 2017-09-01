#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2017/7/19 15:15
# @Author   : zhangjian
# @Site     : 
# @File     : performance.py
# @Purpose  :
# @Software : PyCharm Community Edition
# @Copyright:   (c) zhangjian 2017
# @Licence  :     <your licence>

"""
客户端性能测试工具
"""
import os
import re
import time
from multiprocessing import Process

package_name = "slots"


def cpu_test(test_time):
    i = 0
    cpulist = []
    time_init = int(time.time())
    time_end = time_init + test_time
    current_time = int(time.time())
    while current_time < time_end:
        print ("测试倒计时:%s秒" % (time_end - current_time))
        t = os.popen("adb shell top -m 20 -n 1")
        content = t.readlines()
        t.close()
        # print ("content:"), content

        cpu_info = None
        for item in content:
            if package_name in item:
                cpu_info = item
                break

        if cpu_info == None:
            raise Exception("apk is not lunched")

        # print cpu_info

        all_no = re.findall("\d+\d|\d", cpu_info)
        # print all_no
        pid = int(all_no[0])
        cpu_no = int(all_no[2])
        # print ("Pid = "), pid
        # print ("cpu_no = "), cpu_no
        print time.strftime("%Y-%m-%d-%H:%M:%S:"), ("CPU=%s" % cpu_no) + ("%")
        cpulist.append(cpu_no)
        current_time = int(time.time())

        i += 1
    average_cpu = sum(cpulist) / i
    print ("平均CPU为%s" % average_cpu) + ("%")


def get_pid():
    """
    获取包的pid，每重启一次会变更
    :return: pid
    """
    t = os.popen("adb shell top -m 20 -n 1")
    content = t.readlines()
    t.close()
    cpu_info = None
    for item in content:
        if package_name in item:
            cpu_info = item
            break
    all_no = re.findall("\d+\d|\d", cpu_info)
    pid = int(all_no[0])
    return pid


def psstotal_test(test_time):
    i = 0
    pid = get_pid()
    time_init = int(time.time())
    time_end = time_init + test_time
    current_time = int(time.time())
    psslist = []
    while current_time < time_end:
        t = os.popen("adb shell dumpsys meminfo %s" % pid)
        content = t.readlines()
        t.close()
        for item in content:
            if "TOTAL" in item:
                # print item
                pss_info = item
                break
        pss = re.findall("\d+\d|\d", pss_info)
        psstotal = int(pss[0])
        current_time = int(time.time())
        # print ("测试倒计时:%s秒"%(current_time-time_init))
        print time.strftime("%Y-%m-%d-%H:%M:%S:"), ("PssTotal="), psstotal
        psslist.append(psstotal)
        time.sleep(2)
        i += 1
    maxlist = sorted(psslist, reverse=True)
    average_pss = sum(psslist) / i
    print ("平均PssTotal="), average_pss
    print ("最高PssTotal="), maxlist[0]
    print ("最低PSSTotal="), maxlist[-1]


if __name__ == '__main__':
    test_time = 600
    p1 = Process(target=cpu_test, args=(test_time,))
    p2 = Process(target=psstotal_test, args=(test_time,))
    p1.start()
    p2.start()
