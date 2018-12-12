#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王

from protocol.smsp_http import SMSP_HTTP

ip = 'http://172.16.5.132:19527'


request = {
    "clientid": "b00ii7",
    "password": "aa123456"
}
smsp_http = SMSP_HTTP(interface_name='getbalance', ip=ip, **request)
smsp_http.http_json(**request)
