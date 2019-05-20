# coding:utf-8
from __future__ import print_function
from __future__ import print_function
from __future__ import absolute_import, unicode_literals

import ConfigParser
import os
import json
import re
import socket
import threading
import time
import requests
from socket import *
from threading import Lock
import random
from time import sleep,ctime


# contentdata = { "TerminalIp": "192.168.1.186", "Position": "3,0" }
# r = requests.post("http://127.0.0.1:8000/sdt-hts/hsInterface/", data=contentdata)
#
# contentdata = { "TerminalIp": "192.168.1.110", "Position": "3,1" }
# r = requests.post("http://127.0.0.1:8000/sdt-hts/hsInterface/", data=contentdata)
# print(r)

ip = []
ip.append("192.168.1.186")
ip.append("192.168.1.110")
ip.append("192.168.1.231")
ip.append("192.168.1.234")
ip.append("10.25.16.90")
ip.append("10.25.16.91")
pos = []
pos.append("3,0")
pos.append("3,1")
cnt = 0
while 1:

    contentdata = { "TerminalIp": ip[random.randrange(len(ip))], "Position": pos[random.randrange(len(pos))] }
    r = requests.post("http://127.0.0.1:8000/sdt-hts/hsInterface/", data=contentdata)
    sleep(10.0)

#
# HOST = "192.168.1.206"
# PORT = 5038
# BUFSIZ = 10240
# ADDR = (HOST, PORT)
# tcpCliSock = None
#
#
# def returnCode2Dict(retCode):
#     if type(retCode) is not str:
#         return False
#     s = re.sub(r'\r\n\r\n', '', retCode)
#     a = s.split('\r\n')
#     retDict = {}
#     for item in a:
#         res = re.split(r':', item, 1)
#         if len(res) < 2:
#             pass
#         else:
#             retDict[res[0]] = res[1]
#     return retDict
#
# try:
#     tcpCliSock = socket(AF_INET, SOCK_STREAM)
#     tcpCliSock.connect(ADDR)
#
# except BaseException as e:
#     tcpCliSock = None
#
#
# def loop():
#     global tcpCliSock
#
#     while True:
#         try:
#             if tcpCliSock is None:
#                 print("tcpCliSock is None")
#                 tcpCliSock = socket(AF_INET, SOCK_STREAM)
#                 tcpCliSock.connect(ADDR)
#
#             data = tcpCliSock.recv(BUFSIZ)
#             # print("loop recv:",data)
#             if "RESP_NOTIFY" in data.decode('gb2312'):
#                 continue
#             if "BusinessOperation" in data.decode('gb2312'):
#                 rcv_dict = returnCode2Dict(data.decode('gb2312'))
#
#                 contentdata = { "TerminalIp": rcv_dict["TerminalIp"], "Position": rcv_dict["Position"] }
#                 r = requests.get("http://127.0.0.1:8000/sdt-hts/hsInterface/", data = contentdata)
#                 print(rcv_dict)
#
#         except UnicodeDecodeError as e:
#             print("loop decode error:", e)
#         except BaseException as e:
#             print("loop error:", e)
#             tcpCliSock = None
#             time.sleep(1.0)
#
#     print("out loop!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#
#
# t = threading.Thread(target=loop)
# t.start()
