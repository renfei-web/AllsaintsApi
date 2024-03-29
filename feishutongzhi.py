# _*_ coding: utf-8 _*_
# @Time : 2023/9/21 11:26
# @Author : Ren Fei
# @Version：
# @File : feishutongzhi.py
# @desc :


import sys
import requests
import time
import json

JOB_URL = sys.argv[1]
JOB_NAME = sys.argv[2]
BUILD_NUMBER = sys.argv[3]
GIT_BRANCH = sys.argv[4]
print(JOB_URL, JOB_NAME, BUILD_NUMBER, GIT_BRANCH)


# JOB_URL = "test_url"
# JOB_NAME = "test_job"
# BUILD_NUMBER = "110"
# GIT_BRANCH = "master"

currenttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
url = 'https://open.feishu.cn/open-apis/bot/v2/hook/8dac7896-b332-4adf-9aab-7a9acc7ff533'
method = 'post'
headers = {
   'Content-Type': 'application/json',
   'Accept': '*/*',
}

payload = json.dumps({
    "msg_type": "interactive",
    "card": {
        "config": {
                "wide_screen_mode": True,
                "enable_forward": True
        },
        "elements": [{
                "tag": "div",
                "text": {
                    # 这是卡片的内容，也可以添加其他的内容：比如构建分支，构建编号等
                    "content": "项目名称：" + JOB_NAME + "\n构建编号：第" + BUILD_NUMBER + "次构建\n运行时间：" + currenttime + "\n分支:" + GIT_BRANCH,
                    "tag": "lark_md"
                }
        }, {
                "actions": [{
                        "tag": "button",
                        "text": {
                                "content": "查看测试报告", # 这是卡片的按钮，点击可以跳转到url指向的allure路径
                                "tag": "lark_md"
                        },
                        "url": f"{JOB_URL}/{BUILD_NUMBER}/allure/", # JOB_URL 调用python定义的变量，该url是服务器下的allure路径
                        "type": "default",
                        "value": {}
                }],
                "tag": "action"
        }],
        "header": {
                "title": {
                        "content": JOB_NAME + "构建报告", # JOB_NAME 调用python定义的变量，这是卡片的标题
                        "tag": "plain_text"
                }
        }
    }
})
# res = requests.request(method=method, url=url, headers=headers, json=data)
# print(res)
# print(res.json())
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)



