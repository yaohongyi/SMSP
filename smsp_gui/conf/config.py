#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 姚诚 2017/12/25 16:18 

from configparser import ConfigParser

class Config(object):
    def __init__(self, path):
        self.path = path
        self.config = ConfigParser()
        self.config.read(self.path, encoding="utf-8-sig")

    def get_options(self):
        # 获取information下所有的options
        options = dict(self.config.items('information'))
        # 根据配置文件获取运营商
        operator_dict = {'CMPP':0, 'SGIP':1, 'SMGP':2, 'SMPP':3, 'INLAND':4, 'ALL':5}
        operator = options['operator'][3:]
        options['operator'] = operator_dict[operator]
        sms_type = {'0':0, '4':1, '5':2, '6':3, '7':4, '8':5}
        options['sms_type'] = sms_type[options['sms_type']]
        return options

    def save(self, values):
        for value in values:
            self.config.set(section='information', option=value, value=str(values[value]))
        self.config.write(open(self.path, "w", encoding="utf-8"))

if __name__ == '__main__':
    c = Config(path='config.ini')
    # value = {'ip': '113.31.21.248', 'port': 29524, 'random_mobile': 1, 'mobile_num': 1, 'operator': 'cmpp', 'time_stamp': 1, 'time_sleep': 0, 'send_num': 1, 'to_beautify': 0, 'sms_type': '5', 'clientid': 'b00ii7', 'password': 'aa123456', 'mobile': '13900002222', 'uid': '111', 'extend': '222', 'content': '【都君网】哈哈哈1'}
    # c.save(value)
    c.get_options()
