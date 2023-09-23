# _*_ coding: utf-8 _*_
# @Time : 2023/2/17 16:14
# @Author : Ren Fei
# @Version：
# @File : hot_module.py
# @desc :
# 读取 extract中的 access_token
import yaml
from commons.yaml_util import get_object_path


class HotFunc():
    def read_extract_yaml(self):
        with open(get_object_path() + "/extract.yaml", 'r', encoding="utf-8") as f:
            # yaml文件中读取内容
            msg = yaml.load(stream=f, Loader=yaml.FullLoader)
            return msg["access_token"]

    # 读取config.yaml
    def read_config_yaml(self, node_one, node_two):
        with open(get_object_path() + '/config.yaml', mode="r", encoding='utf-8') as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            return value[node_one][node_two]

