# _*_ coding: utf-8 _*_
# @Time : 2023/2/14 15:47
# @Author : Ren Fei
# @Version：
# @File : time_util.py
# @desc :

import time


# 获取13位时间戳
def get_Milli_Time():
    current_milli_time = int(round(time.time() * 1000))
    return current_milli_time





# if __name__ == '__main__':
    # print(TimeStamp().get_Milli_Time())