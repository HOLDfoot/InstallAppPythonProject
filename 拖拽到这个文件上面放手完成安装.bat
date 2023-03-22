:: 设置编码格式
:: 65001是utf-8 936是gbk 在win10上是utf-8, 在win7上是gbk
chcp 65001

@setlocal enabledelayedexpansion
@echo off
title 安装目录下所有安装包: %1

echo 当前安装目录 %1
echo 当前程序目录 %~dp0

set current_path=%~dp0
set bb=python_exe_path.txt
set "config_path=%current_path%%bb%"
@echo 读取python配置路径
@echo %config_path%

set main_file=main.py
set "main_path=%current_path%%main_file%"
@echo 拼接python的main.py的路径
@echo %main_path%


for /f "delims=" %%i in (%config_path%) do (

rem set start_command=C:\Users\Administrator\AppData\Local\Programs\Python\Python310\python.exe D:\PycharmProjects\InstallAppPythonProject\main.py C:\Users\Administrator\Desktop\测试原始安装包 D:\PycharmProjects\InstallAppPythonProject\
set start_command=%%i %main_path% %1 %current_path%
@echo 执行命令start命令
@echo !start_command!
start !start_command!
rem set start_command=%%i %main_path% %1 %current_path%
rem @echo %%i %main_path% %1 %current_path%
rem echo 调用脚本命令执行: %start_command%
rem start %start_command%
rem start %%i %main_path% C:\Users\Administrator\Desktop\测试原始安装包 %current_path%
rem start %%i main.py %1
rem echo %%i main.py %1
rem start C:\Users\Administrator\AppData\Local\Programs\Python\Python310\python.exe %main_path% C:\Users\Administrator\Desktop\测试原始安装包 %current_path%
)
pause