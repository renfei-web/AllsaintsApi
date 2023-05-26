# _*_ coding: utf-8 _*_
# @Time : 2023/5/24 18:23
# @Author : Ren Fei
# @Version：
# @File : test_gettoken.py
# @desc :
import allure
import pytest
from commons.log_util import Logging
from commons.parametrize_util import read_testcase_yaml
from commons.requests_util import RequestUtil
from readLoads.hot_module import HotFunc

logger = Logging().log("INFO")


@allure.epic("Allsaints_Api_Frame")
@allure.feature("登录模块")
class TestCmsSongApi:
    @allure.story("cms登录接口")
    @allure.title("成功获取token")
    @pytest.mark.first
    @pytest.mark.parametrize("caseInfo", read_testcase_yaml("/datas/get_token/getToken.yaml"))
    def test_get_token(self, caseInfo):
        RequestUtil(HotFunc()).standard_yml(caseInfo)