#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王

from protocol.smsp_http import SMSP_HTTP

interface_name = 'templatesms'

smsp_http = SMSP_HTTP(interface_name=interface_name)
request = {
    'clientid':'b00ii7',
    'password':'aa123456',
    'mobile':'13900003214',
    'templateid':'',
    'param':'',
    'sendtime':'',
    'extend':'',
    'uid':''
}
