#！coding: utf-8
import requests
from lxml import etree

class GetWeather(object):
    def __init__(self):
        self.dict_code = {}

    def set_code(self):
        with open(r"E:\code\citycode.txt", "r") as f:
            for line in f.readlines():
                if line != "\n":
                    L = line.split("=")
                    try:
                        self.dict_code[L[1].strip().decode("gbk")] = L[0]
                    except IndexError:
                        import pdb;pdb.set_trace()

    def get_code(self, city):
        if city in self.dict_code:
            return self.dict_code[city]
        raise Exception(u"城市不存在")

if __name__ == "__main__":
    test = GetWeather()
    test.set_code()
    print test.get_code(u"重庆")


