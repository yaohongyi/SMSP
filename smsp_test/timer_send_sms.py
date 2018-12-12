#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
from protocol.smsp_http import SMSP_HTTP

request = {
        'clientid':'b008l5',
        'password':'aa123456',
        'mobilelist':'',
        'smstype':'0',
        'content':'【都君网】123',
        'sendtime':'2018-08-25 16:04:56',
        'extend':'',
        'uid':'',
        'compress_type':'0'
    }
setting = {
    'random_mobile':1,
    'mobile_num':10,
    'json_beautify':1
}
kwargs = {
    'request':request,
    'setting':setting
}
smsp_http = SMSP_HTTP(interface_name='timer_send_sms',**kwargs)
smsp_http.timer_send_sms()

