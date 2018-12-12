#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 都君丨大魔王

import socket


address = ('172.16.5.132', 19520)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect_ex(address)

while True:
    cmd = input("Please input msg:")
    s.send(cmd.encode())
    data = s.recv(1024)
    print(data.decode('utf-8'))
