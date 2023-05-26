# _*_ coding: utf-8 _*_
# @Time : 2023/5/25 14:29
# @Author : Ren Fei
# @Version：
# @File : test_release_songsheet.py
# @desc :

import allure
import pytest

from commons.log_util import Logging
from commons.parametrize_util import read_testcase_yaml
from commons.requests_util import RequestUtil
from readLoads.hot_module import HotFunc

logger = Logging().log("INFO")



@allure.epic("Allsaints_Api_Frame")
@allure.feature("资源管理--歌单模块")
class TestCmsSongSheet:
    @allure.story("发布歌单按钮")
    @allure.title("发布歌单")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize("caseInfo", read_testcase_yaml("/datas/resource_manage/song_sheet/release_list.yaml"))
    def test_refresh_song(self, caseInfo):
        RequestUtil(HotFunc()).standard_yml(caseInfo)