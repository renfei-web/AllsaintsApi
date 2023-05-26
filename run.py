# _*_ coding: utf-8 _*_
# @Time : 2023/2/14 15:26
# @Author : Ren Fei
# @Version：
# @File : run.py.py
# @desc :
import os
import time
import pytest

from commons.log_util import Logging

logger = Logging().log("INFO")

if __name__ == '__main__':

    pytest.main()

    time.sleep(3)

    os.system("allure generate ./temps -o ./reports --clean")


    # 将JSON文件转换成HTML格式的测试报告（生成JSON文件路径：outputs/reports/allure; 生成HTML报告路径：outputs/reports/html）
    # os.system("allure generate outputs/reports/allure -o outputs/reports/html --clean")
    # 命令：allure generate outputs/reports/allure -o outputs/reports/html --clean
    # 打开测试报告
    # os.system("allure serve outputs/reports/allure")
    # 命令：allure serve outputs/reports/allure













