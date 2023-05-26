# _*_ coding: utf-8 _*_
# @Time : 2023/2/15 10:33
# @Author : Ren Fei
# @Version：
# @File : log_util.py
# @desc :

import traceback
import logging, time, os


class Logging():
    def make_log_dir(self, dirname='logs'): # 创建存放日志的目录，并返回目录的路径
        now_dir = os.path.dirname(__file__)
        father_dir = os.path.split(now_dir)[0]
        path = os.path.join(father_dir, dirname)
        path = os.path.normpath(path)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def get_log_filename(self):  # 创建日志文件的文件名格式，便于区分每天的日志
        filename = "{}.log".format(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
        filename = os.path.join(self.make_log_dir(), filename)
        filename = os.path.normpath(filename)
        return filename

    def log(self, level='INFO'):    # 生成日志的主方法，传入那些级别以上的日志进行处理
        logger = logging.getLogger()   # 创建日志器
        level = getattr(logging, level)   # 获取日志模块的的级别对象属性
        logger.setLevel(level)  # 设置日志级别
        if not logger.handlers:   # 作用：防止重新生成处理器
            sh = logging.StreamHandler()  # 创建控制台日志处理器
            fh = logging.FileHandler(filename=self.get_log_filename(),mode='a',encoding='utf-8') # 创建日志文件处理器

            # 创建格式器
            fmt = logging.Formatter("【%(asctime)s】-【%(levelname)s】-【%(filename)s】-【Line:%(lineno)d】-【Message:%(message)s】")

            # 给处理器添加格式
            sh.setFormatter(fmt=fmt)
            fh.setFormatter(fmt=fmt)

            # 给日志器添加处理器
            logger.addHandler(hdlr=sh)
            logger.addHandler(hdlr=fh)
        return logger   # 返回日志器


if __name__ == '__main__':
    logger = Logging().log(level='DEBUG')  # 调用封装的日志方法，生成处理后的日志器
    logger.debug("1111111111111111111111")  # 使用日志器生成日志
    logger.info("222222222222222222222222")
    logger.error("附件为IP飞机外婆家二分IP文件放")
    logger.warning("3333333333333333333333333333")
    logger.critical("44444444444444444444444444")

