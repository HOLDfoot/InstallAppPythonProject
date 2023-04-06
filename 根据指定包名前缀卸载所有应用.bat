:: 设置编码格式
:: 65001是utf-8 936是gbk 在win10上是utf-8, 在win7上是gbk
chcp 65001

@echo off
title 卸载所有MYT应用

@echo 链接板子开始卸载
for /f "delims=" %%i in (pythonExePath.txt) do (
echo 调用脚本命令执行: %%i uninstallMyt.py
start %%i uninstallMyt.py
)
pause