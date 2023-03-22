# encoding:utf-8
import datetime
import os
import sys
import subprocess
import shutil
from pathlib import Path
import install_after_check

# 当前运行的路径
current_path = os.getcwd()
android_source = "原始安卓包"

def install_file(file):
    # print("install_file: " + file)
    install_after_check.get_package_by_apk(file, current_path)


def install_folder(folder):
    #print("install_folder: " + folder)
    if folder.endswith(".apk"):
        one_file = folder
        install_file(os.path.join(folder, one_file))
        return
    file_list = []
    for root, dirs, files in os.walk(folder):
        file_list = files
        break
    for one_file in file_list:
        install_file(os.path.join(folder, one_file))

if __name__ == '__main__':
    if len(sys.argv) == 3:
        android_path = sys.argv[1]
        current_path = sys.argv[2]
    else:
        android_path = os.path.join(current_path, android_source)
    print("安卓文件路径: " + android_path)
    print("python路径: " + current_path)

    install_folder(android_path)

    # 不关闭窗口
    os.system("pause")
