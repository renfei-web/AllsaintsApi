# _*_ coding: utf-8 _*_
# @Time : 2023/2/15 11:40
# @Author : Ren Fei
# @Version：
# @File : yaml_util.py
# @desc :

import os
# from ruamel import yaml as yam
import yaml

# 执行脚本文件路径
def get_object_path():
    return os.getcwd()

# access_token存储yaml文件
def write_extrict_yaml(data):
    with open(get_object_path() + '/extract.yaml', mode='w', encoding='utf-8') as f:
        value = yaml.dump(stream=f, data=data, allow_unicode=True)
        return value

# 读取yaml测试用例
def read_yaml(path):
    with open(get_object_path() + "\datas\\" + path, 'r', encoding="utf-8") as f:
        # yaml文件中读取内容
        msg = yaml.load(stream=f, Loader=yaml.FullLoader)
        return msg
# 清空yaml
def clear_extract_yaml():
    with open(get_object_path()+'/extract.yaml', mode="w", encoding='utf-8') as f:
        f.truncate()

# 读取用例yaml
def read_data_yaml(yaml_path):
    with open((get_object_path()+yaml_path).replace(r'\\', '/'), mode="r", encoding='utf-8') as f:
        print("***************" + get_object_path() +yaml_path +"***************")
        value = yaml.load(stream=f, Loader=yaml.FullLoader)
        return value


if __name__ == '__main__':
    print(get_object_path())
    # print(get_object_path() + "\datas\\"+ "song_refresh.yaml")
