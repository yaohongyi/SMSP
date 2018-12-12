#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王

import random, base64

class SMSP_Tool(object):
    def random_mobile(self, operator='cmpp'):
        '''
        传入运营商，随机生成运营商的手机号
        :param operator: 运营商代号，移动cmpp，联通sgip，电信smgp，国际smpp，不区分大小写
        :return: 一个指定运营商下的手机号
        '''
        # 定义移动、联通、电信号段
        cmpp_segments = [134, 135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 178, 182, 183, 184, 187, 188,
                         1703, 1705, 1706, 198]
        sgip_segments = [130, 131, 132, 145, 155, 156, 171, 175, 176, 185, 186, 1704, 1707, 1709, 1708, 166]
        smgp_segments = [133, 149, 153, 173, 177, 180, 181, 189, 1700, 1701, 1702, 1731, 199]
        smpp_segments = [32, 33, 44, 61, 62, 63, 84, 93]
        # all_segments = cmpp_segments + sgip_segments + smgp_segments + smpp_segments
        all_segments = cmpp_segments + sgip_segments + smgp_segments
        # 根据参数选择指定运营商的一个号段
        if operator.lower() == 'cmpp':
            mobile_segment = random.choice(cmpp_segments)
        elif operator.lower() == 'sgip':
            mobile_segment = random.choice(sgip_segments)
        elif operator.lower() == 'smgp':
            mobile_segment = random.choice(smgp_segments)
        elif operator.lower() == 'smpp':
            mobile_segment = random.choice(smpp_segments)
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

    def black_list_table_index(self, phone, seed=31):
        '''通过算法算出手机号应该存入到哪张t_sms_blacklist_*黑名单表'''
        phone_hash = 0
        phone = str(phone)
        for i in range(len(phone)):
            phone_hash = phone_hash * seed + int(phone[i]) + 48
        table_index = phone_hash%5 + 1
        print(table_index)
        return table_index

    def insert_black_list(self, mobile_num):
        '''生成插入黑名单的sql'''
        with open('black_list.sql', 'w+') as file:
            for i in range(mobile_num):
                mobile = self.random_mobile(operator='all')
                table_index = self.black_list_table_index(mobile)
                black_list_sql = "insert into t_sms_black_list_{}(clientid,phone,update_date)" \
                                         "values('*',{},now());\n".format(table_index, mobile)
                file.write(black_list_sql)

    def insert_blank_phone(self, mobile_num):
        '''生成插入空号库的sql'''
        with open('blank_phone.sql', 'w+') as file:
            for i in range(mobile_num):
                mobile = self.random_mobile(operator='all')
                blank_phone_sql = "INSERT INTO `t_sms_blank_phone`(`blank_phone`, `update_time`, `operator_id`) " \
                                  "VALUES ({}, now(), 0);\n".format(mobile)
                file.write(blank_phone_sql)

    def unbase64(self, string_object):
        result = base64.b64decode(string_object)
        print(result)
        return result


if __name__ == "__main__":
    smsp_tool = SMSP_Tool()
    # mobile_num = 50000
    # smsp_tool.insert_black_list(mobile_num)
    # smsp_tool.insert_blank_phone(mobile_num)
    # smsp_tool.black_list_table_index(phone=13800000000)

