import configparser
import os


class ReadConfig:
    """定义一个读取配置文件的类"""

    def __init__(self, filepath=None):
        if filepath:
            configpath = filepath
        else:
            root_dir = os.path.dirname(os.path.abspath('.'))
            configpath = os.path.join(root_dir, "config.cfg")
        self.cf = configparser.ConfigParser()
        self.cf.read(configpath ,encoding="utf-8-sig")

    def getpath(self, param):
        value = self.cf.get("path", param)
        return value


def getpath(key):
    root_dir = os.path.dirname(os.path.abspath('.'))
    readcfg = ReadConfig(root_dir + "\\config\\sn_laptop.cfg")
    return readcfg.getpath(key)
