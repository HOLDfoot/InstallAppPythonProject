# encoding:utf-8
import os
import subprocess
import util.file_string_util as file_string_util

def get_package_by_apk(apk_path, current_path):
    aapt_path = os.path.join(current_path, "aapt2.exe")
    wrap_path = ""
    if apk_path.__contains__(" "):
        wrap_path = '"' + apk_path + '"'
    else:
        wrap_path = apk_path
    exec_command = aapt_path + " dump badging " + wrap_path
    print("exec_command: " + exec_command)
    p = subprocess.Popen(exec_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 响应码及内容
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        output = str(stdout)
        splits = output.split("'")
        one_package_name = splits[1]
        print("获取包信息成功: " + one_package_name)
        return one_package_name
    else:
        print("=================================================================")
        print("获取包信息失败: " + wrap_path)
        print(stdout)
        print(stderr)
        print(p.returncode)
        print("=================================================================")
        return ""

def get_replace_install_config(current_path):
    replace_install_flag = False
    replace_install_flag_file = current_path + "/config/是否替换安装配置文件.txt"
    if os.path.isfile(replace_install_flag_file):
        file_object = open(replace_install_flag_file, 'r')  # 创建一个文件对象，也是一个可迭代对象
        try:
            all_the_text = file_object.read()  # 结果为str类型
            replace_install_flag = all_the_text == "1"
        finally:
            file_object.close()
    print("replace_install_flag: " + str(replace_install_flag))
    return replace_install_flag

def find_myt_package(current_path):
    adb_path = os.path.join(current_path, "adb.exe")
    exec_command = '{} shell pm list packages'.format(adb_path)
    print("exec_command: " + exec_command)
    p = subprocess.Popen(exec_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 响应码及内容
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        print("获取系统包名, 执行成功")
    else:
        print("获取系统包名, 执行失败")
        return []
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
    myt_packages = []
    for i in range(app_installed_num):
        one_package_name = splits[i][8:]
        prefix = file_string_util.get_spec_package_prefix(current_path)
        if one_package_name.lower().startswith(prefix):
            myt_packages.append(one_package_name)
    print("myt_packages: " + str(myt_packages))
    return myt_packages

if __name__ == '__main__':
    get_replace_install_config()
    find_myt_package()

    apk_path = "bagua.apk"
    one_package_name = get_package_by_apk(apk_path)
    print("one_package_name: " + str(one_package_name))
    # 不关闭窗口
    os.system("pause")
