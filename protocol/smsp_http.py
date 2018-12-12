#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王
import base64
import gzip
import json
import random
import time
import requests
import hashlib

from PyQt5 import QtCore


class SMSP_HTTP(QtCore.QThread):
    text = QtCore.pyqtSignal(str)

    def __init__(self, interface_name='sendsms', ip='http://172.16.5.132:19524', **kwargs):
        super().__init__()
        self.ip = ip
        self.kwargs = kwargs
        self.interface_name = interface_name
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json;charset=utf-8'}

    def password_md5(self, password):
        '''http请求密码加密'''
        if password != "":
            password_encode = password.encode('utf-8')
            password_md5 = hashlib.md5(password_encode).hexdigest()
        else:
            password_md5 = password
        return password_md5

    def http_json(self, json_beautify=True, **request):
        ''''''
        if self.interface_name == 'sendsms':
            url = '{}/smsp/sms-partner/access/{}/sendsms'.format(self.ip, request['clientid'])
        elif self.interface_name == 'getmo':
            url = '{}/sms-partner/report/{}/getmo'.format(self.ip, request['clientid'])
        elif self.interface_name == 'getreport':
            url = '{}/sms-partner/report/{}/getreport'.format(self.ip, request['clientid'])
        elif self.interface_name == 'getbalance':
            url = '{}/sms-partner/report/{}/getbalance'.format(self.ip, request['clientid'])
        elif self.interface_name == 'timer_send_sms':
            url = '{}/sms-partner/access/{}/timer_send_sms'.format(self.ip, request['clientid'])
        elif self.interface_name == 'templatesms':
            url = '{}/sms-partner/access/{}/templatesms'.format(self.ip, request['clientid'])
        else:
            url = ''
            print("请确认{}接口名称是否存在！！！".format(self.interface_name))
        if url:
            request['password'] = self.password_md5(password=request['password'])
            body = json.dumps(request, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
            try:
                response = requests.post(url, data=body.encode('utf-8'), headers=self.headers).json()
                if json_beautify:
                    request = json.dumps(request, indent=4, ensure_ascii=False, separators=(',', ':'))
                    response = json.dumps(response, indent=4, ensure_ascii=False, separators=(',', ':'))
                print('【请求内容】：')
                print(request)
                print('【响应内容】：')
                print(response)
                print('—' * 50)
                self.text.emit('【请求消息】：')
                self.text.emit(str(request))
                self.text.emit('')
                self.text.emit('【响应消息】：')
                self.text.emit(str(response))
                self.text.emit('—' * 40)
                return request, response
            except:
                self.text.emit('请求{}超时,请检查IP和端口是否错误！'.format(url))
                self.text.emit('—' * 40)
                print('请求{}超时,请检查IP和端口是否错误！'.format(url))

    def random_mobile(self, operator='cmpp'):
        '''
        传入运营商，随机生成运营商的手机号
        :param operator: 运营商代号，移动cmpp，联通sgip，电信smgp，国际smpp，不区分大小写
        :return: 一个指定运营商下的手机号
        '''
        # 定义移动、联通、电信、国际号段
        cmpp_segments = [134, 135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 178, 182, 183, 184, 187, 188,
                         1703, 1705, 1706, 198]
        sgip_segments = [130, 131, 132, 145, 155, 156, 171, 175, 176, 185, 186, 1704, 1707, 1709, 1708, 166]
        smgp_segments = [133, 149, 153, 173, 177, 180, 181, 189, 1700, 1701, 1702, 1731, 199]
        smpp_segments = [32, 33, 44, 61, 62, 63, 84, 93]
        inland_segments = cmpp_segments + sgip_segments + smgp_segments
        all_segments = cmpp_segments + sgip_segments + smgp_segments + smpp_segments
        # 根据参数选择指定运营商的一个号段
        if operator.upper().count('CMPP'):
            mobile_segment = random.choice(cmpp_segments)
        elif operator.upper().count('SGIP'):
            mobile_segment = random.choice(sgip_segments)
        elif operator.upper().count('SMGP'):
            mobile_segment = random.choice(smgp_segments)
        elif operator.upper().count('SMPP'):
            mobile_segment = random.choice(smpp_segments)
        elif operator.upper().count('INLAND'):
            mobile_segment = random.choice(inland_segments)
        else:
            mobile_segment = random.choice(all_segments)
        # 根据号段算出最大值和最小值
        if len(str(mobile_segment)) in (2, 3):
            mobile_min = mobile_segment * 100000000
            mobile_max = mobile_min + 99999999
        else:
            mobile_min = mobile_segment * 10000000
            mobile_max = mobile_min + 9999999
        if len(str(mobile_segment)) == 2:
            random_mobile = '00' + str(random.randint(mobile_min, mobile_max))
        else:
            random_mobile = str(random.randint(mobile_min, mobile_max))
        return random_mobile

    def best_send(self):
        '''强化版的http协议短信下行'''
        request = self.kwargs['request']
        setting = self.kwargs['setting']
        content_len = len(request['content'])
        # 发送N条短信
        for i in range(setting['send_num']):
            # 是否随机生成指定运营商手机号
            if setting['random_mobile'] == True:
                request['mobile'] = ''
                mobile_list = []
                for i in range(setting['mobile_num']):
                    mobile_list.append(self.random_mobile(setting['operator']))
                    request['mobile'] = ','.join(mobile_list)
            else:
                pass
            if setting['time_stamp'] == True:
                # 短信内容加时间戳，时间戳格式
                now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 时间戳
                request['content'] = request['content'][:content_len] + now_time
            else:
                pass
            self.http_json(json_beautify=setting['json_beautify'], **request)
            time.sleep(setting['time_sleep'])

    def timer_send_sms(self):
        request = self.kwargs['request']
        setting = self.kwargs['setting']
        content_len = len(request['content'])
        if setting['random_mobile'] == True:
            mobile = []
            for i in range(setting['mobile_num']):
                num = random.randint(13000000000, 13999999999)
                mobile.append(str(num))
            mobile_list = ','.join(mobile)
        else:
            mobile_list = request['mobile']
        gzip_mobile_list = gzip.compress(bytes(mobile_list.encode('utf-8')))
        request['mobilelist'] = base64.b64encode(gzip_mobile_list).decode('utf-8')
        if setting['time_stamp'] == True:
            # 短信内容加时间戳，时间戳格式
            now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 时间戳
            request['content'] = request['content'][:content_len] + now_time
        else:
            pass
        self.http_json(**request)

    def templatesms(self):
        request = self.kwargs['request']
        setting = self.kwargs['setting']
        # 发送N条短信
        for i in range(setting['send_num']):
            # 是否随机生成指定运营商手机号
            if setting['random_mobile'] == True:
                request['mobile'] = ''
                mobile_list = []
                for i in range(setting['mobile_num']):
                    mobile_list.append(self.random_mobile(setting['operator']))
                    request['mobile'] = ','.join(mobile_list)
            else:
                pass
            self.http_json(json_beautify=setting['json_beautify'], **request)
            time.sleep(setting['time_sleep'])

    def run(self):
        if self.interface_name == 'sendsms':
            self.best_send()
        elif self.interface_name == 'timer_send_sms':
            self.timer_send_sms()
        elif self.interface_name == 'templatesms':
            self.templatesms()
        else:
            self.http_json(**self.kwargs)

if __name__ == '__main__':
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
