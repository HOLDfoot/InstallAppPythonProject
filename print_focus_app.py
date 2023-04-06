# encoding:utf-8
import os
import subprocess

# 当前运行的路径
current_path = os.getcwd()

if __name__ == '__main__':
    adb_path = os.path.join(current_path, "adb.exe")
    exec_command = adb_path + " shell dumpsys window"
    # print("exec_command: " + exec_command)
    p = subprocess.Popen(exec_command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid = p.pid
    # 响应码及内容
    stdout, stderr = p.communicate()
    # print(stdout)
    if p.returncode == 0:
        print("获取系统当前应用信息: ")
        out_message_str = str(stdout)
        len_end = len(out_message_str) - 1
        out_message_lines = out_message_str[2:len_end]
        out_message_lines_array = out_message_lines.split("\\r\\n")
        # print("len: " + str(len(out_message_lines_array)))
        for line in out_message_lines_array:
            # print(line)
            if line.__contains__("mCurrentFocus"):
                print(line)
                print("解析出包名: ")
                splits = line.split("/")[0].split(" ")
                print(splits[len(splits) - 1])
    else:
        print(stderr)
    # 不关闭窗口
    os.system("pause")
