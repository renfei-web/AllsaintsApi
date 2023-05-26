# _*_ coding: utf-8 _*_
# @Time : 2023/2/15 16:02
# @Author : Ren Fei
# @Version：
# @File : requests_util.py
# @desc :

import json
import re
import traceback
import jsonpath as jsonpath
import requests
from commons.log_util import Logging
from commons.yaml_util import write_extrict_yaml


logger = Logging().log("INFO")


class RequestUtil():

    # session关联会话,，session默认的情况下会自动关联cookie
    session = requests.session()

    def __init__(self, obj):
        self.obj = obj

    def standard_yml(self, caseinfo):
        try:
            logger.info("-------------------接口测试开始-------------------")
            caseinfo_keys = caseinfo.keys()
            # 先判断一级关键字
            if "name" in caseinfo_keys and "request" in caseinfo_keys:
                # 判断二级关键字，method,url
                request_keys = caseinfo["request"].keys()
                if "method" in request_keys and "url" in request_keys:
                    # 发送请求
                    base_url = caseinfo.pop("base_url")
                    name = caseinfo.pop("name")
                    method = caseinfo["request"].pop("method")
                    url = caseinfo["request"].pop("url")
                    url = base_url + url

                    res = self.send_request(name, method, url, **caseinfo["request"])

                    res_code = res.status_code
                    res_text = res.text
                    res_json = ""

                    try:
                        res_json = res.json()
                        # logger.info(f"响应结果{res_json}")
                        # return res_json
                    except Exception as e:
                        logger.info("返回的结果不是json格式")

                    if "extract" in caseinfo_keys:
                        write_extrict_yaml(res_json)
                    # if "extract" in caseinfo_keys:
                    #     for key, value in caseinfo["extract"].items():
                    #         if "(.*?)" in value or "(.+?)" in value:  # 正则
                    #             zz_value = re.search(value, return_text)
                    #             if zz_value:
                    #                 extract_value = {key: zz_value.group(1)}
                    #                 write_extract_yaml(extract_value)
                    #         else:
                    #             # jsonpath
                    #             js_value = jsonpath.jsonpath(return_json, value)
                    #             if js_value:
                    #                 extract_value = {key: js_value[0]}
                    #                 write_extract_yaml(extract_value)
                    # 断言
                    return_code = res_code
                    expect_result = caseinfo["validate"]
                    really_result = res_json
                    self.assert_result(expect_result, really_result, return_code)
                else:
                    logger.error("在request下必须包含:method,url")
            else:
                logger.error("一级参数格式不正确，检查是否包含name,request,validate关键字")
        except Exception as e:
            logger.error(f"规范yaml测试用例standard_yml异常：{traceback.format_exc()}")


    def replace_value(self, data):
        if data:
            # 保存数据类型
            data_type = type(data)
            if isinstance(data, dict) or isinstance(data, list):
                str_data = json.dumps(data)
            else:
                str_data = data
            # 替换值
            for cs in range(1, str_data.count("${") + 1):
                if "${" in str_data and "}" in str_data:
                    start_index = str_data.index("${")
                    end_index = str_data.index("}", start_index)
                    old_value = str_data[start_index:end_index + 1]

                    func_name = old_value[old_value.index("${") + 2:old_value.index("(")]
                    args_name = old_value[old_value.index("(") + 1:old_value.index(")")]

                    if args_name != "":
                        args_value2 = args_name.split(",")
                        new_value = getattr(self.obj, func_name)(*args_value2)
                    else:
                        new_value = getattr(self.obj, func_name)()

                    if isinstance(new_value, int) or isinstance(new_value, float):
                        str_data = str_data.replace('"' + old_value + '"', str(new_value))
                    else:
                        str_data = str_data.replace(old_value, new_value)
            if isinstance(data, dict) or isinstance(data, list):
                data = json.loads(str_data)
            else:
                data = data_type(str_data)
        return data

    # 请求统一封装
    def send_request(self, name, method, url, **kwargs):
        # 请求方法处理
        method = str(method).lower()
        url = self.replace_value(url)
        # 参数替换  kwargs可能是 json data params headers
        if kwargs:
            for key, value in kwargs.items():
                if key in ["headers", "json", "data", "params"]:
                    kwargs[key] = self.replace_value(value)
                elif key == "files":
                    for file_key, file_path in value.items():
                        value[file_key] = open(file_path, 'rb')
        logger.info(f"接口名称：{name}")
        logger.info(f"请求方式：{method}")
        logger.info(f"请求url：{url}")
        if "headers" in kwargs.keys():
            logger.info(f"请求头：{kwargs['headers']}")
        if "params" in kwargs.keys():
            logger.info(f"请求参数：{kwargs['params']}")
        elif "json" in kwargs.keys():
            logger.info(f"请求参数：{kwargs['json']}")
        elif "data" in kwargs.keys():
            logger.info(f"请求参数：{kwargs['data']}")
        elif "files" in kwargs.keys():
            logger.info(f"文件上传：{kwargs['files']}")

        res = RequestUtil.session.request(method=method, url=url, **kwargs)

        return res


    # 对不同断言进行封装，如果增加断言继续增加判断
    def assert_result(self,expect_result,really_result,return_code):
        try:
            logger.info(f"预期结果：{expect_result}")
            logger.info(f"实际结果：{really_result}")
            all_flag = 0
            # print(expect_result)
            for expect in expect_result:
                for key, value in expect.items():
                    # print(assert_key,assert_value)
                    if key == "equals":
                        flag = self.equals_assert(value, return_code, really_result)
                        all_flag = all_flag+flag
                    elif key=="contains":
                        flag = self.contains_assert(value, really_result)
                        all_flag = all_flag + flag
            assert all_flag == 0
            logger.info(f"接口测试成功")
            logger.info("-------------------接口测试结束-------------------\n")

        except Exception as e:
            logger.info(f"接口测试失败")
            logger.info("-------------------接口测试结束-------------------\n")
            logger.error(f"断言assert_result异常：{traceback.format_exc()}")



    # 相等断言
    def equals_assert(self,value,return_code,really_result):
        flag = 0
        for assert_key, assert_value in value.items():
            if assert_value:
                if assert_key == "status_code":
                    # 返回状态码断言
                    if return_code != assert_value:
                        flag += 1
                        logger.error(f"断言失败：返回状态码是{return_code}不等于{assert_value}")
                else:
                    # 返回值相等断言
                    lists = jsonpath.jsonpath(really_result,'$..{}'.format(assert_key))
                    if lists:
                        if assert_value not in lists:
                            flag += 1
                            logger.error(f"断言失败：{assert_key}的值不等于{assert_value}")
                    else:
                        flag += 1
                        logger.error(f"断言失败：返回结果中不包含{assert_key}")
            else:
                flag += 1
                logger.error(f"断言失败：断言格式不正确，equals为空")
        return flag


    # 包含断言
    def contains_assert(self,value,really_result):
        flag = 0
        if str(value) not in str(really_result):
            flag += 1
            logger.error("断言失败："+str(value)+"不在返回结果中")
        return flag
