:: 设置编码格式
:: 65001是utf-8 936是gbk 在win10上是utf-8, 在win7上是gbk
chcp 65001

@echo off
title 安装'安装原始文件'并获取安装状态

@echo 读取python_exe_path.txt开始安装
for /f "delims=" %%i in (python_exe_path.txt) do (
echo 调用脚本命令执行: %%i main.py
start %%i main.py
)
pause