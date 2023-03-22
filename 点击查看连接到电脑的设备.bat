:: 设置编码格式
:: 65001是utf-8 936是gbk 在win10上是utf-8, 在win7上是gbk
chcp 65001

@echo off
title 查看当前连接到电脑的设备

@echo 请确保设备已经连接到电脑
adb.exe devices
pause