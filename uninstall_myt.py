# encoding:utf-8
import datetime
import os
import sys
import subprocess
import file_string_util

# 当前运行的路径
current_path = os.getcwd()

global count_of_uninstall
global count_of_uninstall_fail
global count_of_uninstall_success

global uninstall_myt_type # 0是全部, 1是游戏

def uninstall_package(package_name):
    global count_of_uninstall_fail
    global count_of_uninstall_success
    global count_of_uninstall
    count_of_uninstall = count_of_uninstall + 1

    adb_path = os.path.join(current_path, "adb.exe")
    exec_command = adb_path + " uninstall " + package_name
    # print("exec_command: " + exec_command)
    p = subprocess.Popen(exec_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid = p.pid
    # 响应码及内容
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        count_of_uninstall_success = count_of_uninstall_success + 1
        print("卸载成功: " + package_name)
    else:
        print("=================================================================")
        print("卸载失败: " + package_name)
        count_of_uninstall_fail = count_of_uninstall_fail + 1
        print(stdout)
        print(stderr)
        print(p.returncode)
        print("=================================================================")

def find_package():
    adb_path = os.path.join(current_path, "adb.exe")
    print("find_package: " + adb_path)
    exec_command = '{} shell pm list packages'.format(adb_path)
    print("exec_command: " + exec_command)
    p = subprocess.Popen(exec_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid = p.pid
    print("subprocess pid: " + str(pid))
    # 响应码及内容
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        print("获取系统包名, 执行成功")
    else:
        print("获取系统包名, 执行失败")
    print(stdout)
    print(stderr)
    print(p.returncode)
    output = str(stdout)
    output_len = len(output)
    output = output[2:output_len - 1]
    splits = output.split("\\r\\n")
    splits_len = len(splits)
    app_installed_num = splits_len - 1
    # print("splits: " + str(splits))
    print("app_installed_num: " + str(app_installed_num))
    for i in range(app_installed_num):
        one_package_name = splits[i][8:]
        prefix = file_string_util.get_spec_package_prefix(current_path)
        global uninstall_myt_type
        if uninstall_myt_type == 1:
            prefix = prefix + "game"
        if one_package_name.lower().startswith(prefix):
            uninstall_package(one_package_name)

if __name__ == '__main__':
    global uninstall_myt_type
    if len(sys.argv) == 2:
        uninstall_myt_type = int(sys.argv[1])
    else:
        uninstall_myt_type = 0

    global count_of_uninstall
    global count_of_uninstall_fail
    global count_of_uninstall_success
    count_of_uninstall = 0
    count_of_uninstall_fail = 0
    count_of_uninstall_success = 0

    find_package()
    print("一共成功检测应用{}个".format(str(count_of_uninstall)))
    print("一共卸载失败应用{}个".format(str(count_of_uninstall_fail)))
    print("一共卸载成功应用{}个".format(str(count_of_uninstall_success)))
    # 不关闭窗口
    os.system("pause")
