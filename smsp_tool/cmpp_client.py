#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王

'''CMPP转发工具'''

import requests

def send_cmpp_client(url='http://172.16.5.132:29999', **kwargs):
    request_url = "http://{}?phone={phone}&content={content}&displaynum={displaynum}&channelid={channelid}".format \
        (url,
         phone=kwargs['phone'],
         content=kwargs['content'],
         displaynum=kwargs['displaynum'],
         channelid=kwargs['channelid'])
    print(request_url)
    response = requests.get(request_url).text
    return response

if __name__ == "__main__":
    content = "【都君网】北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你，北京欢迎你。"
    kwargs = {
        "content": content,
        "displaynum": 11,
        "phone": "13900001562",
        "channelid": 8801
    }
    send_cmpp_client(**kwargs)

