#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王

from protocol.smsp_http import SMSP_HTTP


request = {
    'mobile': '13912340001',
    'clientid': 'b00kx2',
    'uid': '11',
    'smstype': '0',  # 0：通知短信，4：验证码短信，5：营销短信，6：告警短信，7：USSD，8：闪信
    'password': 'aa123456',
    'extend': '11',
    'content': '【都君网】'
}
setting = {
    'random_mobile':0,  # 是否需要生成随机手机号
    'mobile_num':0,  # 随机生成手机号个数
    'operator':"all",  # 要生成手机号运营商类型：移动-cmpp、联通-sgip、电信-smgp、国际-smpp，其他则为4种运营商类型随机
    'time_stamp':1,  # 短信内容结尾添加时间戳
    'time_sleep':1,  # 发送间隔
    'send_num':1,  # 发送次数
    'json_beautify':1  # 请求、响应json格式化打印
}
kwargs = {
    'request':request,
    'setting':setting
}

smsp_http = SMSP_HTTP(**kwargs)
smsp_http.best_send()
