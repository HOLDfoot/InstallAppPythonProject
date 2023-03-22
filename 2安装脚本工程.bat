:: 设置编码格式
:: 65001是utf-8 936是gbk 在win10上是utf-8, 在win7上是gbk
chcp 65001

@setlocal enabledelayedexpansion
@echo off
title 安装本工程所需的python路径

echo 输出所有python路径到all_python_path.txt文件
where python > all_python_path.txt
set num=0
echo 以下是所有python版本的位置, 自动选择第一个作为python路径
for /f "delims=" %%i in (all_python_path.txt) do (
    set /a num+=1
    echo 第!num!行
    echo %%i
    if !num! equ 1 (
        echo 选择上面的python路径作为脚本执行路径
        echo %%i > python_exe_path.txt
    )
)
echo !!!必须使用python3, 如果装了多个python, 请手动将python3的路径放到python_exe_path.txt中
pause
