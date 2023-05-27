# _*_ coding: utf-8 _*_
# @Time : 2023/5/24 18:26
# @Author : Ren Fei
# @Version：
# @File : test_song_refresh.py
# @desc :


import allure
import pytest

from commons.log_util import Logging
from commons.parametrize_util import read_testcase_yaml
from commons.requests_util import RequestUtil
from readLoads.hot_module import HotFunc

logger = Logging().log("INFO")



@allure.epic("Allsaints_Api_Frame")
@allure.feature("资源管理--歌曲模块")
class TestCmsSongSheet:
    @allure.story("同步按钮接口")
    @allure.title("同步歌曲信息")
    @pytest.mark.resource
    @pytest.mark.parametrize("caseInfo", read_testcase_yaml("/datas/resource_manage/song/song_refresh.yaml"))
    def test_refresh_song(self, caseInfo):
        RequestUtil(HotFunc()).standard_yml(caseInfo)
