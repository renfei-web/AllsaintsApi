# _*_ coding: utf-8 _*_
# @Time : 2023/2/18 11:06
# @Author : Ren Fei
# @Version：
# @File : conftest.py
# @desc :
import pytest

from commons.yaml_util import clear_extract_yaml


@pytest.fixture(scope="session", autouse=True)
def auto_extract_yaml():
    # get_token()
    # # print("fixture前置---------------")

    clear_extract_yaml()
    # print("fixture后置置---------------")