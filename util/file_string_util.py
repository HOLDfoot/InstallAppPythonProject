# encoding:utf-8
import os

def get_spec_package_prefix(current_path):
    sub_file_path = "/config/指定包名前缀.txt"
    spec_package_prefix = "com." # 默认值
    delay_check_time_file = os.path.join(current_path, sub_file_path)
    if os.path.isfile(delay_check_time_file):
        file_object = open(delay_check_time_file, 'r')  # 创建一个文件对象，也是一个可迭代对象
        try:
            all_the_text = file_object.read()  # 结果为str类型
            if all_the_text != "":
                spec_package_prefix = str(all_the_text)
        finally:
            file_object.close()
    print("spec_package_prefix: " + str(spec_package_prefix))
    return spec_package_prefix