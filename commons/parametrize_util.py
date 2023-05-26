# _*_ coding: utf-8 _*_
# @Time : 2023/5/25 11:58
# @Author : Ren Fei
# @Version：
# @File : parametrize_util.py
# @desc :
import json
import traceback

import yaml

from commons.yaml_util import get_object_path, read_data_yaml
from commons.log_util import Logging

logger = Logging().log("INFO")

def read_testcase_yaml(yaml_path):
    try:
        with open(get_object_path() + yaml_path, mode="r", encoding='utf-8') as f:
            caseinfo = yaml.load(stream=f, Loader=yaml.FullLoader)
            if len(caseinfo) >= 2:
                return caseinfo
            else:
                if "parameterize" in dict(*caseinfo).keys():
                    new_caseinfo = parame_ddt(*caseinfo)
                    return new_caseinfo
                else:
                    return caseinfo
    except Exception as e:
        logger.erro(f"读取测试用例方法read_testcase_yaml异常: {traceback.format_exc()}")

def parame_ddt(caseinfo):
    try:
        caseinfo_str = json.dumps(caseinfo)
        if "parameterize" in caseinfo.keys():
            # 数据驱动
            for parame_key, parame_value in caseinfo["parameterize"].items():
                key_list = parame_key.split('-')
                data_list = read_data_yaml(parame_value)
                length_flag = True
                for data in data_list:
                    if len(data) != len(key_list):
                        length_flag = False
                        break
                # print("--------------------替换值---------------------------------")
                new_caseinfo = []
                if length_flag:
                    # 替换值
                    for x in range(1, len(data_list)):  # 对嵌套列表中的case进行遍历
                        temp_caseinfo = caseinfo_str
                        for y in range(0, len(data_list[x])):  # 对每条case元素进行遍历
                            if data_list[0][y] in key_list:
                                # 替换原始yaml中的$ddt{}
                                if isinstance(data_list[x][y], int) or isinstance(data_list[x][y], float):
                                    temp_caseinfo = temp_caseinfo.replace('"' + "$ddt{" + data_list[0][y] + "}" + '"', str(data_list[x][y]))
                                else:
                                    temp_caseinfo = temp_caseinfo.replace("$ddt{" + data_list[0][y] + "}", str(data_list[x][y]))
                        new_caseinfo.append(json.loads(temp_caseinfo))
                return new_caseinfo
        else:
            return caseinfo
    except Exception as e:
        logger.error(f"数据驱动方法parame_ddt异常：{traceback.format_exc()}")