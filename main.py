# encoding:utf-8
import datetime
import os
import sys
import subprocess
from subprocess import Popen
import shutil
from pathlib import Path
import install_after_check
from threading import Timer
import time
import signal

# 当前延时检查的时间
global delay_check_time
delay_check_time = 100
# 当前运行的路径
current_path = os.getcwd()
android_source = "原始安卓包"
android_success = "安装成功文件"
android_fail = "安装失败文件"
global count_of_install
global count_of_install_fail
global count_of_install_success
global replace_install_flag
global myt_packages
global global_input_apk


def install_file(input_apk, output_excel):
    global count_of_install
    global count_of_install_fail
    global count_of_install_success
    global replace_install_flag
    global myt_packages
    global delay_check_time

    print("install_file: " + input_apk)
    count_of_install = count_of_install + 1

    file_path = Path(input_apk)
    file_name = file_path.name

    apk_package = install_after_check.get_package_by_apk(input_apk, current_path)
    line = file_name + "\t" + str(apk_package)
    if not replace_install_flag:  # 不强制安装就检查, 如果有就不安装
        if myt_packages.__contains__(apk_package):
            count_of_install_success = count_of_install_success + 1
            line = line + "\t" + "已经安装"
            line = line + "\n"
            excel_file = open(output_excel, "a")
            excel_file.writelines(line)
            excel_file.close()
            print("已经安装")
            return

    adb_path = os.path.join(current_path, "adb.exe")
    cmd_file = input_apk
    if input_apk.__contains__(" "):
        cmd_file = '"' + input_apk + '"'
    exec_command = adb_path + " install -r " + cmd_file
    print("exec_command: " + exec_command)
    p = subprocess.Popen(exec_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid = p.pid
    print("subprocess pid: " + str(pid))
    install_start = int(time.time())
    stats = os.stat(input_apk)
    file_size_in_mb = 1.0 * stats.st_size / 1000000
    # delay_check_time决定这个时间的比例, 比如100的时候, 90M的文件超时时间是9s
    the_file_over_time = int(file_size_in_mb * delay_check_time / 100 * 1 / 10)
    if the_file_over_time <= 30:
        the_file_over_time = 30
    print("file_size_in_mb: " + str(file_size_in_mb))
    print("the_file_over_time: " + str(the_file_over_time))
    check_timer = Timer(the_file_over_time, check_dead_process, args=[input_apk, output_excel, install_start, pid])
    check_timer.start()
    install_start = int(time.time())
    print("正在安装, 将打印安装输出, 安装错误, 安装返回值")
    if count_of_install == 1:
        print("如果这个地方等待超过10s请按一次Enter")
    # 还没有执行安装
    # 响应码及内容
    stdout, stderr = p.communicate()
    # 已经执行完成
    print(stdout)
    print(stderr)
    print(p.returncode)
    check_timer.cancel()
    install_end = int(time.time())
    install_duration = install_end - install_start
    print("install_file 消耗安装时间: " + str(install_duration))
    is_canceled = False
    if install_duration >= the_file_over_time:
        if p.returncode == signal.CTRL_BREAK_EVENT:
            is_canceled = True
    fail_copy = os.path.join(current_path, android_fail, file_name)
    if p.returncode == 0:
        count_of_install_success = count_of_install_success + 1
        # shutil.copy(file, success_copy)
        line = line + "\t" + "安装成功"
    else:
        count_of_install_fail = count_of_install_fail + 1
        shutil.copy(input_apk, fail_copy)
        if "b''" == stderr.__str__():  # p.returncode != 1
            line = line + "\t" + "无法安装" + str(p.returncode) + "\t" + stdout.__str__()
        else:
            line = line + "\t" + "安装失败\t" + stderr.__str__()
    line = line + "\n"
    excel_file = open(output_excel, "a")
    excel_file.writelines(line)
    excel_file.close()
    return is_canceled  # 2代表被杀死 signal.SIGINT


def print_red(str2):
    print("\033[0;31;40m", str2, "\033[0m")


def check_dead_process(input_apk, output_excel, install_start, pid):
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    install_end = int(time.time())
    install_duration = install_end - install_start
    print("input_apk       : " + str(input_apk))
    print("install_start   : " + str(install_start))
    print("install_duration: " + str(install_duration))
    print("killing process : " + str(pid))
    print("当前文件安装被阻塞: " + str(install_duration) + "秒")
    # os.kill(pid, signal.CTRL_BREAK_EVENT)
    Popen("TASKKILL /F /PID {pid} /T".format(pid=pid))
    print("已经杀死当前安装进程")
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")


def retry_install(input_apk, output_excel):
    is_canceled = install_file(input_apk, output_excel)
    while is_canceled:
        print("retry_install 安装失败")
        delay_retry = 10
        print_red("retry_install 延迟" + str(delay_retry) + "秒重试")
        time.sleep(delay_retry)
        print("retry_install 开始重试 install_file")
        is_canceled = install_file(input_apk, output_excel)
        # 把上次安装失败的增量减去
        global count_of_install
        global count_of_install_fail
        count_of_install = count_of_install - 1
        count_of_install_fail = count_of_install_fail - 1


def install_folder(folder, output_excel):
    print("install_folder: " + folder)
    if folder.endswith(".apk"):
        one_file = folder
        input_apk = os.path.join(folder, one_file)
        # install_file_with_check(input_apk, output_excel)
        retry_install(input_apk, output_excel)
        return
    file_list = []
    for root, dirs, files in os.walk(folder):
        file_list = files
        break
    for one_file in file_list:
        if str(one_file).endswith(".apk"):
            input_apk = os.path.join(folder, one_file)
            # install_file_with_check(input_apk, output_excel)
            retry_install(input_apk, output_excel)


def set_delay_check_time_config(current_path):
    global delay_check_time
    delay_check_time_file = current_path + "/config/一个安装超时百分比系数.txt"
    if os.path.isfile(delay_check_time_file):
        file_object = open(delay_check_time_file, 'r')  # 创建一个文件对象，也是一个可迭代对象
        try:
            all_the_text = file_object.read()  # 结果为str类型
            if all_the_text != "":
                delay_check_time = int(all_the_text)
        finally:
            file_object.close()
    print("delay_check_time: " + str(delay_check_time))
    return delay_check_time


if __name__ == '__main__':
    if len(sys.argv) == 3:
        android_path = sys.argv[1]
        current_path = sys.argv[2]
    else:
        android_path = os.path.join(current_path, android_source)
    print("安装文件路径: " + android_path)
    print("python路径: " + current_path)

    # 删除android_success和android_fail
    # android_success_path = os.path.join(current_path, android_success)
    android_fail_path = os.path.join(current_path, android_fail)
    # if os.path.exists(android_success_path):
    #     shutil.rmtree(android_success_path)
    if os.path.exists(android_fail_path):
        shutil.rmtree(android_fail_path)
    # 创建新的空目录
    # os.mkdir(android_success_path)
    os.mkdir(android_fail_path)

    latest_date_time = datetime.datetime.now()
    output_excel_name = "安装信息-{}.xls".format(latest_date_time.__str__()[5:16])
    output_excel_name = output_excel_name.replace(":", "-")
    output_excel_name = output_excel_name.replace(" ", "-")
    install_record_path = os.path.join(current_path, "安装记录")
    if not os.path.exists(install_record_path):
        os.mkdir(install_record_path)
    output_excel = os.path.join(install_record_path, output_excel_name)
    print("输出的Excel: " + output_excel)
    excel_file = open(output_excel, "w+")
    line = "安装文件名\t包名信息\t安装结果\t安装错误信息\n"
    excel_file.writelines(line)
    excel_file.close()

    set_delay_check_time_config(current_path)
    global replace_install_flag
    replace_install_flag = install_after_check.get_replace_install_config(current_path)
    global myt_packages
    myt_packages = install_after_check.find_myt_package(current_path)

    global count_of_install
    global count_of_install_fail
    global count_of_install_success
    count_of_install = 0
    count_of_install_fail = 0
    count_of_install_success = 0

    install_folder(android_path, output_excel)

    global global_input_apk
    global_input_apk = ""
    print("一共发现安装包{}个".format(str(count_of_install)))
    print("一共失败安装包{}个".format(str(count_of_install_fail)))
    print("一共成功安装包{}个".format(str(count_of_install_success)))

    # 不关闭窗口
    os.system("pause")
