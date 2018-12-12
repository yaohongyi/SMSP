#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王

import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import *
from smsp_gui.conf.config import Config
from protocol.smsp_http import SMSP_HTTP

config = Config('./conf/config.ini')


class Client(QWidget):
    def __init__(self, *args, **kwargs):
        # 读取配置文件所有值
        self.options = config.get_options()
        super().__init__(*args, **kwargs)
        self.all_init()

    def all_init(self):
        '''打开客户端时初始化需要的动作'''
        self.setup_ui(self)
        self.read_config()
        self.check_content_length()
        self.mobile_set()
        self.chose_templatesms()
        self.interface_change()

    def setup_ui(self, frame):
        '''创建窗口元素'''
        self.setFixedSize(1000, 600)
        self.setWindowTitle('SMSP短信发送工具v20180827（姚诚）')
        self.setWindowIcon(QtGui.QIcon('.\icon\LOGO.png'))
        self.client_grid = QGridLayout(frame)
        # 【基本设置】分组框
        self.server_GroupBox = QGroupBox('【基本设置】')
        self.client_grid.addWidget(self.server_GroupBox, 0, 0, 1, 3)
        self.http_type_Label = QLabel('请求类型：')
        self.http_type_ComboBox = QComboBox()
        self.http_type_ComboBox.addItems(['HTTP', 'HTTPS'])
        self.ip_Label = QLabel('* 请求地址：')
        self.ip_LineEdit = QLineEdit()
        self.ip_LineEdit.setPlaceholderText('ip')
        self.port_Label = QLabel('* 请求端口：')
        self.port_LineEdit = QLineEdit()
        self.port_LineEdit.setPlaceholderText('port')
        self.random_mobile_QLabel = QLabel('号码随机：')
        self.random_mobile_ComboBox = QComboBox()
        self.random_mobile_ComboBox.addItems(['不随机', '随机'])
        self.random_mobile_ComboBox.currentTextChanged.connect(self.mobile_set)
        self.mobile_num_QLabel = QLabel('号码个数：')
        self.mobile_num_SpinBox = QSpinBox()
        self.mobile_num_SpinBox.setRange(1, 1000000)
        self.operator_QLabel = QLabel('运营商：')
        self.operator_ComboBox = QComboBox()
        self.operator_ComboBox.addItems(['移动-CMPP', '联通-SGIP', '电信-SMGP', '国际-SMPP', '国内-INLAND', '全部-ALL'])
        self.time_stamp_QLabel = QLabel('时间戳：')
        self.time_stamp_ComboBox = QComboBox()
        self.time_stamp_ComboBox.addItems(['不需要', '需要'])
        self.time_stamp_ComboBox.currentIndexChanged.connect(self.check_content_length)
        self.send_interval_QLabel = QLabel('发送间隔：')
        self.send_interval_SpinBox = QSpinBox()
        self.send_interval_SpinBox.setRange(0, 300)
        self.send_interval_SpinBox.setSingleStep(1)
        self.send_num_QLabel = QLabel('发送次数：')
        self.send_num_SpinBox = QSpinBox()
        self.send_num_SpinBox.setRange(1, 1000)
        self.send_num_SpinBox.setSingleStep(1)
        self.to_beautify_QLabel = QLabel('日志美化：')
        self.to_beautify_ComboBox = QComboBox()
        self.to_beautify_ComboBox.addItems(['不美化', '美化'])
        # 【请求参数】分组框
        self.parameter_GroupBox = QGroupBox('【请求参数】')
        self.client_grid.addWidget(self.parameter_GroupBox, 1, 0, 1, 3)
        self.interface_name_Label = QLabel('* 接口名称：')
        self.interface_name_ComboBox = QComboBox()
        self.interface_name_ComboBox.addItems(['下行短信', '查询余额', '拉取上行', '拉取状态报告', '定时短信', '模板短信'])
        self.interface_name_ComboBox.currentIndexChanged.connect(self.interface_change)
        self.interface_name_ComboBox.currentIndexChanged.connect(self.chose_templatesms)
        self.sms_type_Label = QLabel('* 短信类型：')
        self.sms_type_ComboBox = QComboBox()
        self.sms_type_ComboBox.addItems(['0-通知', '4-验证码', '5-营销', '6-告警', '7-USSD', '8-闪信'])
        self.client_id_Label = QLabel('* 发送账号：')
        self.client_id_LineEdit = QLineEdit()
        self.password_Label = QLabel('* 密码：')
        self.password_LineEdit = QLineEdit()
        self.password_LineEdit.setToolTip('明文密码自动加密！')
        self.mobile_Label = QLabel('* 手机号码：')
        self.mobile_LineEdit = QLineEdit()
        self.mobile_LineEdit.setPlaceholderText('多个手机号码使用英文逗号分隔')
        self.uid_Label = QLabel('UID：')
        self.uid_LineEdit = QLineEdit()
        self.extend_Label = QLabel('扩展端口：')
        self.extend_LineEdit = QLineEdit()
        self.content_Label = QLabel('* 短信内容：')
        self.content_TextEdit = QTextEdit()
        self.content_TextEdit.setPlaceholderText('正确短信内容由（签名+内容）组成')
        self.content_TextEdit.setToolTip('正确短信内容由（签名+内容）组成！')
        self.content_length_Label = QLabel()
        self.content_TextEdit.textChanged.connect(self.check_content_length)
        self.sendtime_Label = QLabel('* 发送时间：')
        self.sendtime_DateTimeEdit = QDateTimeEdit(QtCore.QDateTime.currentDateTime())  # 获取当前时间
        self.sendtime_DateTimeEdit.setDisplayFormat('yyyy-MM-dd hh:mm:ss')  # 时间格式化

        # 【保存】按钮
        self.save_PushButton = QPushButton('保存(Ctrl+S)')
        self.client_grid.addWidget(self.save_PushButton, 2, 0, 1, 1)
        self.save_PushButton.setShortcut('Ctrl+S')
        self.save_PushButton.clicked.connect(self.save_config)
        # 【发送】按钮
        self.send_PushButton = QPushButton('发送(F10)')
        self.client_grid.addWidget(self.send_PushButton, 2, 1, 1, 1)
        self.send_PushButton.setShortcut('F10')
        self.send_PushButton.clicked.connect(self.chose_interface)
        # 【清除】按钮
        self.clear_PushButton = QPushButton('清除(Ctrl+L)')
        self.client_grid.addWidget(self.clear_PushButton, 2, 2, 1, 1)
        self.clear_PushButton.setShortcut('Ctrl+L')
        self.clear_PushButton.clicked.connect(self.clear_log)
        # 【日志打印】消息打印窗口
        self.log_GroupBox = QGroupBox('【日志打印】')
        self.client_grid.addWidget(self.log_GroupBox, 0, 3, 3, 4)
        self.log_TextBrowser = QTextBrowser()

        '''对窗口元素进行布局'''
        # 【基本设置】分组框进行布局
        self.server_grid = QGridLayout(self.server_GroupBox)
        self.server_grid.addWidget(self.random_mobile_QLabel, 0, 0)
        self.random_mobile_QLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.server_grid.addWidget(self.random_mobile_ComboBox, 0, 1)
        self.server_grid.addWidget(self.mobile_num_QLabel, 0, 2)
        self.mobile_num_QLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.server_grid.addWidget(self.mobile_num_SpinBox, 0, 3)
        self.server_grid.addWidget(self.operator_QLabel, 1, 0)  # 手机号运营商
        self.operator_QLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.server_grid.addWidget(self.operator_ComboBox, 1, 1)
        self.server_grid.addWidget(self.time_stamp_QLabel, 1, 2)  # 时间戳
        self.time_stamp_QLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.server_grid.addWidget(self.time_stamp_ComboBox, 1, 3)
        self.server_grid.addWidget(self.send_interval_QLabel, 2, 0)  # 发送间隔
        self.send_interval_QLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.server_grid.addWidget(self.send_interval_SpinBox, 2, 1)
        self.server_grid.addWidget(self.send_num_QLabel, 2, 2)  # 发送次数
        self.send_num_QLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.server_grid.addWidget(self.send_num_SpinBox, 2, 3)
        self.server_grid.addWidget(self.to_beautify_QLabel, 3, 0)  # 请求&响应格式化
        self.to_beautify_QLabel.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.server_grid.addWidget(self.to_beautify_ComboBox, 3, 1)
        self.server_grid.addWidget(self.http_type_Label, 3, 2)
        self.http_type_Label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.server_grid.addWidget(self.http_type_ComboBox, 3, 3)
        self.server_grid.addWidget(self.ip_Label, 4, 0)
        self.server_grid.addWidget(self.ip_LineEdit, 4, 1)
        self.server_grid.addWidget(self.port_Label, 4, 2)
        self.server_grid.addWidget(self.port_LineEdit, 4, 3)
        # 【请求参数】分组框进行布局
        self.parameter_grid = QGridLayout(self.parameter_GroupBox)
        self.parameter_grid.addWidget(self.interface_name_Label, 0, 0)
        self.parameter_grid.addWidget(self.interface_name_ComboBox, 0, 1)
        self.parameter_grid.addWidget(self.sms_type_Label, 0, 2)
        self.parameter_grid.addWidget(self.sms_type_ComboBox, 0, 3)
        self.parameter_grid.addWidget(self.client_id_Label, 1, 0)
        self.parameter_grid.addWidget(self.client_id_LineEdit, 1, 1)
        self.parameter_grid.addWidget(self.password_Label, 1, 2)
        self.password_Label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.parameter_grid.addWidget(self.password_LineEdit, 1, 3)
        self.parameter_grid.addWidget(self.mobile_Label, 2, 0)
        self.parameter_grid.addWidget(self.mobile_LineEdit, 2, 1, 1, 3)
        self.parameter_grid.addWidget(self.uid_Label, 3, 0)
        self.uid_Label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.parameter_grid.addWidget(self.uid_LineEdit, 3, 1)
        self.parameter_grid.addWidget(self.extend_Label, 3, 2)
        self.extend_Label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignRight)
        self.parameter_grid.addWidget(self.extend_LineEdit, 3, 3)
        self.parameter_grid.addWidget(self.content_Label, 5, 0)
        self.parameter_grid.addWidget(self.content_TextEdit, 5, 1, 7, 3)
        self.parameter_grid.addWidget(self.content_length_Label, 12, 1, 1, 3)
        self.parameter_grid.addWidget(self.sendtime_Label, 13, 0, 1, 3)
        self.parameter_grid.addWidget(self.sendtime_DateTimeEdit, 13, 1, 1, 1)
        # 【日志打印】
        self.log_grid = QGridLayout(self.log_GroupBox)
        self.log_grid.addWidget(self.log_TextBrowser)

    def check_content_length(self):
        '''根据时间戳和短信内容，检查实际短信内容长度'''
        value = self.get_value()
        time_stamp_length = 19
        if value['time_stamp']:
            content_length = len(value['content']) + time_stamp_length
            self.content_length_Label.setText('「有时间戳」短信内容长度为{}。'.format(content_length))
        else:
            content_length = len(value['content'])
            self.content_length_Label.setText('「无时间戳」短信内容长度为{}。'.format(content_length))
        self.content_length_Label.setStyleSheet("color:blue")  # 设置字体颜色

    def read_config(self):
        '''打开客户端时读取配置文件信息'''
        # 读取“基本设置”信息
        self.random_mobile_ComboBox.setCurrentIndex(int(self.options['random_mobile']))
        self.mobile_num_SpinBox.setValue(int(self.options['mobile_num']))
        self.operator_ComboBox.setCurrentIndex(self.options['operator'])
        self.time_stamp_ComboBox.setCurrentIndex(int(self.options['time_stamp']))
        self.send_interval_SpinBox.setValue(int(self.options['time_sleep']))
        self.send_num_SpinBox.setValue(int(self.options['send_num']))
        self.to_beautify_ComboBox.setCurrentIndex(int(self.options['to_beautify']))
        self.ip_LineEdit.setText(self.options['ip'])
        self.port_LineEdit.setText(self.options['port'])
        self.http_type_ComboBox.setCurrentIndex(int(self.options['http_type']))
        # 读取“请求参数”信息
        self.sms_type_ComboBox.setCurrentIndex(self.options['sms_type'])
        self.client_id_LineEdit.setText(self.options['clientid'])
        self.password_LineEdit.setText(self.options['password'])
        self.mobile_LineEdit.setText(self.options['mobile'])
        self.uid_LineEdit.setText(self.options['uid'])
        self.extend_LineEdit.setText(self.options['extend'])
        self.content_TextEdit.setText(self.options['content'])

    def save_config(self):
        '''保存客户端信息到配置文件'''
        value = self.get_value()
        self.save_thread = Save_Thread(value)
        self.save_thread.start()

    def get_value(self):
        '''获取客户端所有字段值'''
        value = {}
        # 获取“请求地址”
        value['http_type'] = self.http_type_ComboBox.currentIndex()
        value['ip'] = self.ip_LineEdit.text()
        value['port'] = self.port_LineEdit.text()
        # 获取“发送设置”
        value['random_mobile'] = self.random_mobile_ComboBox.currentIndex()
        value['mobile_num'] = int(self.mobile_num_SpinBox.text())
        value['operator'] = self.operator_ComboBox.currentText()
        value['time_stamp'] = self.time_stamp_ComboBox.currentIndex()
        value['time_sleep'] = int(self.send_interval_SpinBox.text())
        value['send_num'] = int(self.send_num_SpinBox.text())
        value['to_beautify'] = int(self.to_beautify_ComboBox.currentIndex())
        # 获取请求接口名称
        interface_index = self.interface_name_ComboBox.currentIndex()
        if interface_index == 0:
            interface_name = 'sendsms'
        elif interface_index == 1:
            interface_name = 'getbalance'
        elif interface_index == 2:
            interface_name = 'getmo'
        elif interface_index == 3:
            interface_name = 'getreport'
        elif interface_index == 4:
            interface_name = 'timer_send_sms'
        else:
            interface_name = 'templatesms'
        value['interface_name'] = interface_name
        # 获取“请求参数”
        if interface_index == 5:
            value['templateid'] = self.sms_type_ComboBox.text()
        else:
            value['sms_type'] = self.sms_type_ComboBox.currentText()
            value['sms_type'] = value['sms_type'][0]
        value['clientid'] = self.client_id_LineEdit.text()
        value['password'] = self.password_LineEdit.text()
        value['mobile'] = self.mobile_LineEdit.text()
        value['uid'] = self.uid_LineEdit.text()
        value['extend'] = self.extend_LineEdit.text()
        value['content'] = self.content_TextEdit.toPlainText()
        value['sendtime'] = self.sendtime_DateTimeEdit.text()
        return value

    def mobile_set(self):
        '''根据是否“随机号码”来设定“运营商”、“手机号码”是否可以编辑'''
        random_mobile = self.random_mobile_ComboBox.currentIndex()
        if random_mobile == 0:
            self.operator_ComboBox.setDisabled(True)
            self.mobile_LineEdit.setDisabled(False)
            self.mobile_num_SpinBox.setDisabled(True)
        else:
            self.operator_ComboBox.setDisabled(False)
            self.mobile_LineEdit.setDisabled(True)
            self.mobile_num_SpinBox.setDisabled(False)

    def clear_log(self):
        '''清除日志区域信息'''
        self.log_TextBrowser.clear()

    def print_log(self, text):
        '''日志区域打印'''
        self.log_TextBrowser.append(text)

    def interface_change(self):
        '''根据“接口名称”值的改变，调整客户端可编辑内容'''
        interface_index = self.interface_name_ComboBox.currentIndex()
        if interface_index == 0:
            self.random_mobile_ComboBox.setDisabled(False)
            self.mobile_num_SpinBox.setDisabled(False)
            self.operator_ComboBox.setDisabled(False)
            self.time_stamp_ComboBox.setDisabled(False)
            self.send_interval_SpinBox.setDisabled(False)
            self.send_num_SpinBox.setDisabled(False)
            self.to_beautify_ComboBox.setDisabled(False)
            self.sms_type_ComboBox.setDisabled(False)
            self.mobile_set()
            self.uid_LineEdit.setDisabled(False)
            self.extend_LineEdit.setDisabled(False)
            self.content_TextEdit.setDisabled(False)
            self.sendtime_DateTimeEdit.setDisabled(True)
        elif interface_index in (1, 2, 3):
            self.random_mobile_ComboBox.setDisabled(True)
            self.mobile_num_SpinBox.setDisabled(True)
            self.operator_ComboBox.setDisabled(True)
            self.time_stamp_ComboBox.setDisabled(True)
            self.send_interval_SpinBox.setDisabled(True)
            self.send_num_SpinBox.setDisabled(True)
            self.to_beautify_ComboBox.setDisabled(True)
            self.sms_type_ComboBox.setDisabled(True)
            self.mobile_LineEdit.setDisabled(True)
            self.uid_LineEdit.setDisabled(True)
            self.extend_LineEdit.setDisabled(True)
            self.content_TextEdit.setDisabled(True)
            self.sendtime_DateTimeEdit.setDisabled(True)
        elif interface_index == 4:
            self.random_mobile_ComboBox.setDisabled(False)
            self.mobile_num_SpinBox.setDisabled(False)
            self.operator_ComboBox.setDisabled(True)
            self.time_stamp_ComboBox.setDisabled(False)
            self.send_interval_SpinBox.setDisabled(True)
            self.send_num_SpinBox.setDisabled(True)
            self.to_beautify_ComboBox.setDisabled(True)
            self.sms_type_ComboBox.setDisabled(False)
            self.mobile_LineEdit.setDisabled(True)
            self.uid_LineEdit.setDisabled(False)
            self.extend_LineEdit.setDisabled(False)
            self.content_TextEdit.setDisabled(False)
            self.sendtime_DateTimeEdit.setDisabled(False)
        else:
            self.random_mobile_ComboBox.setDisabled(False)
            self.mobile_num_SpinBox.setDisabled(False)
            self.operator_ComboBox.setDisabled(False)
            self.time_stamp_ComboBox.setDisabled(True)
            self.send_interval_SpinBox.setDisabled(False)
            self.send_num_SpinBox.setDisabled(False)
            self.to_beautify_ComboBox.setDisabled(False)
            self.sms_type_ComboBox.setDisabled(False)
            self.mobile_set()
            self.uid_LineEdit.setDisabled(False)
            self.extend_LineEdit.setDisabled(False)
            self.content_TextEdit.setDisabled(False)
            self.sendtime_DateTimeEdit.setDisabled(True)

    def chose_templatesms(self):
        '''当选择“模板短信”接口时，客户端元素需要产生变化'''
        interface_index = self.interface_name_ComboBox.currentIndex()
        if interface_index == 5:
            self.sms_type_Label.setText('* 模板ID：')
            self.sms_type_ComboBox = QLineEdit()
            self.parameter_grid.addWidget(self.sms_type_ComboBox, 0, 3)
            self.content_Label.setText('* 模板参数：')
            self.content_TextEdit.setPlaceholderText(
                '1）多个参数值以英文分号分隔；\n2）参数值顺序与模板中变量顺序相对应；\n3）参数值个数必须与模板中变量个数一致；\n4）格式为“参数值;参数值;参数值”的方式；')
            self.content_TextEdit.setToolTip(
                '1）多个参数值以英文分号分隔；\n2）参数值顺序与模板中变量顺序相对应；\n3）参数值个数必须与模板中变量个数一致；\n4）格式为“参数值;参数值;参数值”的方式；')
        else:
            self.sms_type_Label.setText('* 短信类型：')
            self.sms_type_ComboBox = QComboBox()
            self.sms_type_ComboBox.addItems(['0-通知', '4-验证码', '5-营销', '6-告警', '7-USSD', '8-闪信'])
            self.parameter_grid.addWidget(self.sms_type_ComboBox, 0, 3)
            if interface_index in (1, 2, 3):
                self.sms_type_ComboBox.setDisabled(True)
            self.content_Label.setText('* 短信内容：')
            self.content_TextEdit.setPlaceholderText('正确短信内容由（签名+内容）组成')
            self.content_TextEdit.setToolTip('正确短信内容由（签名+内容）组成！')

    def chose_interface(self):
        '''根据选择的“接口名称”调用不同的接口发送短信'''
        value = self.get_value()
        interface_name = value['interface_name']
        if interface_name == 'sendsms':
            self.send_sms()
        elif interface_name == 'timer_send_sms':
            self.timer_sms()
        elif interface_name == 'templatesms':
            self.template_sms()
        else:
            self.mo_balance_report()

    def template_sms(self):
        value = self.get_value()
        request = {
            'mobile': value['mobile'],
            'clientid': value['clientid'],
            'uid': value['uid'],
            'templateid': value['templateid'],
            'password': value['password'],
            'extend': value['extend'],
            'content': value['content']
        }
        setting = {
            'random_mobile': value['random_mobile'],  # 是否需要生成随机手机号
            'mobile_num': value['mobile_num'],  # 随机生成手机号个数
            'operator': value['operator'],  # 要生成手机号运营商类型：移动-cmpp、联通-sgip、电信-smgp、国际-smpp，其他则为4种运营商类型随机
            'time_sleep': value['time_sleep'],  # 发送间隔
            'send_num': value['send_num'],  # 发送次数
            'json_beautify': value['to_beautify']  # 请求、响应json格式化打印
        }
        kwargs = {
            'request': request,
            'setting': setting
        }
        if value['http_type'] == 0:
            ip = 'http://{}:{}'.format(value['ip'], value['port'])
        else:
            ip = 'https://{}:{}'.format(value['ip'], value['port'])
        self.send_thread = SMSP_HTTP(interface_name=value['interface_name'], ip=ip, **kwargs)
        self.send_thread.text.connect(self.print_log)
        self.send_thread.start()

    def mo_balance_report(self):
        '''查询上行、查询余额、查询状态报告'''
        value = self.get_value()
        kwargs = {
            'clientid': value['clientid'],
            'password': value['password']
        }
        if value['http_type'] == 0:
            ip = 'http://{}:{}'.format(value['ip'], value['port'])
        else:
            ip = 'https://{}:{}'.format(value['ip'], value['port'])
        self.send_thread = SMSP_HTTP(interface_name=value['interface_name'], ip=ip, **kwargs)
        self.send_thread.text.connect(self.print_log)
        self.send_thread.start()

    def timer_sms(self):
        value = self.get_value()
        print(value)
        request = {
            'mobile': value['mobile'],
            'clientid': value['clientid'],
            'uid': value['uid'],
            'smstype': value['sms_type'],
            'password': value['password'],
            'extend': value['extend'],
            'content': value['content'],
            'sendtime': value['sendtime']
        }
        setting = {
            'random_mobile': value['random_mobile'],
            'mobile_num': value['mobile_num'],
            'json_beautify': value['to_beautify'],
            'time_stamp': value['time_stamp']
        }
        kwargs = {
            'request': request,
            'setting': setting
        }
        if value['http_type'] == 0:
            ip = 'http://{}:{}'.format(value['ip'], value['port'])
        else:
            ip = 'https://{}:{}'.format(value['ip'], value['port'])
        self.send_thread = SMSP_HTTP(interface_name=value['interface_name'], ip=ip, **kwargs)
        self.send_thread.text.connect(self.print_log)
        self.send_thread.start()

    def send_sms(self):
        value = self.get_value()
        request = {
            'mobile': value['mobile'],
            'clientid': value['clientid'],
            'uid': value['uid'],
            'smstype': value['sms_type'],
            'password': value['password'],
            'extend': value['extend'],
            'content': value['content']
        }
        setting = {
            'random_mobile': value['random_mobile'],  # 是否需要生成随机手机号
            'mobile_num': value['mobile_num'],  # 随机生成手机号个数
            'operator': value['operator'],  # 要生成手机号运营商类型：移动-cmpp、联通-sgip、电信-smgp、国际-smpp，其他则为4种运营商类型随机
            'time_stamp': value['time_stamp'],  # 短信内容结尾添加时间戳
            'time_sleep': value['time_sleep'],  # 发送间隔
            'send_num': value['send_num'],  # 发送次数
            'json_beautify': value['to_beautify']  # 请求、响应json格式化打印
        }
        kwargs = {
            'request': request,
            'setting': setting
        }
        if value['http_type'] == 0:
            ip = 'http://{}:{}'.format(value['ip'], value['port'])
        else:
            ip = 'https://{}:{}'.format(value['ip'], value['port'])
        self.send_thread = SMSP_HTTP(interface_name=value['interface_name'], ip=ip, **kwargs)
        self.send_thread.text.connect(self.print_log)
        self.send_thread.start()


class Save_Thread(QtCore.QThread):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def run(self):
        config.save(self.value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    client = Client()
    client.show()
    sys.exit(app.exec_())
