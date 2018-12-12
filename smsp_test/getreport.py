#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王

from protocol.smsp_http import SMSP_HTTP

ip = 'http://172.16.5.132:19527'
smsp_http = SMSP_HTTP(ip)

request = {
    "clientid": "b00ii7",
    "password": "aa123456"
}

smsp_http.http_json(interface_name='getreport', **request)
