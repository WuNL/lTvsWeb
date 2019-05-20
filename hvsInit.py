# -*- coding: UTF-8 -*-
from socket import *
from base import hvs_pb2
import time
from time import sleep
import os,re
import subprocess
os.chdir('/home/sdt/workspace/lTvsWeb')
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'lTvsWeb.settings')
import django
django.setup()

from base.models import *
from config.models import *


def handelDevice(devMsg, gpuCount,monitorList):
    devDict = {'gpuSeq': gpuCount}
    devInfoList = re.split('\n', devMsg)
    for item in devInfoList:
        if len(item) == 0 or item == '\n':
            continue
        col = re.split(':', item)
        devDict[(col[0]).strip()] = col[1]
    monitorList.append(devDict)


dustMsgPat = '  Name.*\n.*\n.*\n.*Number of Display Devices: \d+\n'

deviceSplitPat = '  Display Device \d+ \(TV-\d+\):\n'
def handelGpu(gpuMsg, gpuCount,monitorList):
    # print gpuMsg
    result = re.sub(dustMsgPat, '', gpuMsg)
    # print "result= \n",(result)
    result1 = re.split(deviceSplitPat, result)
    for dev in result1:
        if len(dev) == 0:
            continue
        handelDevice(dev, gpuCount,monitorList)
def checkMonitor():
    output = subprocess.Popen('nvidia-xconfig --query-gpu-info', \
                              shell=True, \
                              stdout=subprocess.PIPE).communicate()[0]
    splitpat = 'GPU #\d+:\n'

    res0 = re.sub('Number of GPUs: \d+', '', output)
    res1 = re.sub('\n\n', '\n', res0)
    res2 = re.split(splitpat, res1)
    monitorList = []
    count = 0
    for gpu in res2:
        if len(gpu) == 0 or gpu == '\n':
            continue
        handelGpu(gpu, count,monitorList)
        count += 1
    i = 0
    print monitorList
    channel.objects.all().update(active=False)
    for item in monitorList:
        if channel.objects.filter(pk = (int(i)+1)).count() != 0:
            cn = channel.objects.get(pk = (int(i)+1))
            cn.name = u"通道"+str(i+1)
            cn.monitorName = monitorList[i]['EDID Name']
            cn.resolution = monitorList[i]['Preferred Width']+monitorList[i]['Preferred Height']
            cn.GPUSeq = monitorList[i]['gpuSeq']
            cn.freshRate = monitorList[i]['Preferred VertRefresh']
            cn.active = True
            cn.save()
            i+=1
    return monitorList

if terminalArray.objects.count()<21:
	for i in range(1,22):
		c = terminalArray.objects.get_or_create(pk=int(i))[0]
		c.save()
		if i == 21:
			c.name=u"fuliu"
			c.status=True
			c.save()

######


PORT = 12310
HOST="localhost"
print "screen port is ",PORT
ADDR=(HOST,PORT)


taMsgToSend = hvs_pb2.WrapperMessage()
for i in range(1,21):
	t = terminalArray.objects.get(pk=i)
	temp = taMsgToSend.ta.terminal.add()
	temp.id = t.pk
	if t.ip != None:
		temp.ip = str(t.ip)
	else:
		temp.ip = ""
	if t.name != None:
		temp.name = t.name.encode('utf-8')
	else:
		temp.name = "".encode('utf-8')
	temp.tstatus = t.status
print taMsgToSend
taContent = taMsgToSend.SerializeToString()

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)
tcpCliSock.send(taContent)
tcpCliSock.close()

print checkMonitor()
# 发给每个屏幕
for screen in channel.objects.filter(active=True):
# for screen in channel.objects.all():
#################
	try:
		msgToSend = hvs_pb2.WrapperMessage()
		msgToSend.cpl.id = int(screen.pk)
		msgToSend.cpl.saperateNumber = int(screen.saperateNumber)
		msgToSend.cpl.style = 1
		msgToSend.cpl.inuse = screen.inUse
		msgToSend.cpl.active = screen.active
		msgToSend.cpl.pollingTime = int(screen.pollingTime)
		msgToSend.cpl.isPolling = screen.polling
		if screen.pollingPos == None:
			screen.pollingPos = "1:-1, 2:-1, 3:-1, 4:-1, 5:-1, 6:-1, 7:-1, 8:-1, 9:-1, 10:-1, 11:-1, 12:-1, 13:-1, 14:-1, 15:-1, 16:-1, 17:-1, 18:-1, 19:-1, 20:-1,"
			screen.save()
		if screen.pollingPos == "":
			screen.pollingPos = "1:-1, 2:-1, 3:-1, 4:-1, 5:-1, 6:-1, 7:-1, 8:-1, 9:-1, 10:-1, 11:-1, 12:-1, 13:-1, 14:-1, 15:-1, 16:-1, 17:-1, 18:-1, 19:-1, 20:-1,"
			screen.save()
		rawPosition = screen.pollingPos
		posList = rawPosition.split(" ")
		for i in range(1,21):
			clip = str(i)+":"
			currentPos = re.sub(clip,'',posList[i-1])
			posList[i-1] = currentPos
			# print i,"----",posList[i-1]
			clip = ","
			currentPos = re.sub(clip,' ',posList[i-1])
			posList[i-1] = currentPos
			# print i,"----",posList[i-1]
		for item in posList:
			msgToSend.cpl.terminalID.append(str(item))
		# print msgToSend
		pollingContent = msgToSend.SerializeToString()
		tcpCliSock = socket(AF_INET,SOCK_STREAM)
		tcpCliSock.connect(ADDR)
		tcpCliSock.send(pollingContent)
		tcpCliSock.close()
	except Exception as e2:
		print "send screen id %d error"%int(screen.pk),e2
		errorlist.append(e2)
