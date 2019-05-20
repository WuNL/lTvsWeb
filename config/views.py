# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from base.models import *
from config.models import *
from config.forms import *
from django.http import HttpResponse, HttpResponseServerError
from django.http import HttpResponseRedirect

import re,os
import subprocess
from django.core import serializers
import os
import zipfile
import StringIO
import datetime
import base.hvs_pb2
from socket import *
# Create your views here.




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

#-----------------------------------------------------------------------------------#

@login_required
@csrf_exempt
def getMonitorInfo(request):
    if request.POST:
        try:
            ret=checkMonitor()
            print ret
            if ret != False:
                return HttpResponse(u"刷新显示器成功")
            else:
                print e
                raise Exception(u"未知错误！")
        except Exception as e:
            return HttpResponse(u"刷新显示器not成功")

    elif request.GET:
        # 初始化
        if channel.objects.all().count() == 0:
            for i in range(8):
                channelInstance = channel(pk = int(i+1),name = u"通道"+str(i+1), saperateNumber=4, content=" ",polling=False,pollingPos="1:-1, 2:-1, 3:-1, 4:-1, 5:-1, 6:-1, 7:-1, 8:-1, 9:-1, 10:-1, 11:-1, 12:-1, 13:-1, 14:-1, 15:-1, 16:-1, 17:-1, 18:-1, 19:-1, 20:-1,")
                channelInstance.save()
        try:
            ret = checkMonitor()
            channelList = channel.objects.filter(active = True)
            print channelList
            json_reply = serializers.serialize("json",channelList)
            return HttpResponse(json_reply)
        except Exception as e:
            print e
            return HttpResponse(u"刷新显示器not成功")
    return render(request,'config/getMonitorInfo.html')

import os

@login_required
@csrf_exempt
def configSystem(request):
    if request.POST:
        if request.POST.__contains__("resetDatabase")==True and request.POST['resetDatabase'] == 'True':
            print "RESET"
            userLogInstance = userLog(user= request.user,target=u'系统',content=u'重置数据库')
            userLogInstance.save()
            shutil.copyfile("../db.sqlite3","./db.sqlite3")
            return HttpResponseRedirect('/sdt-hts/')
        if request.POST.__contains__("remoteShutdown")==True and request.POST['remoteShutdown'] == 'True':
            print "remoteShutdown"
            import os
            userLogInstance = userLog(user= request.user,target=u'系统',content=u'远程关机')
            userLogInstance.save()
            os.system("shutdown -s -t 00")
            return HttpResponseRedirect('/sdt-hts/')
        if request.POST.__contains__("remoteRestart")==True and request.POST['remoteRestart'] == 'True':
            print "remoteRestart"
            import os
            userLogInstance = userLog(user= request.user,target=u'系统',content=u'远程重启')
            userLogInstance.save()
            os.system("shutdown -r -t 00")
            return HttpResponseRedirect('/sdt-hts/')
        if request.POST.__contains__("initTVS")==True and request.POST['initTVS'] == 'True':
            print "initTVS"
            import os
            import subprocess
            os.chdir("/home/sdt/workspace/lTvsWeb")
            print subprocess.Popen("/usr/bin/python hvsInit.py",stdout=subprocess.PIPE, shell=True)
        if request.POST.__contains__("start1")==True and request.POST['start1'] == 'True':
            print "start1"
            # start window 1
            import os
            import subprocess
            os.chdir("/home/sdt/workspace/lTvsWeb")
            window1 = channel.objects.get(pk=int(1))
            window1.inUse = True
            window1.save()
            print subprocess.Popen("/usr/bin/python hvsInit.py",stdout=subprocess.PIPE, shell=True)

        if request.POST.__contains__("start2")==True and request.POST['start2'] == 'True':
            print "start2"
            # start window 1
            import os
            import subprocess
            os.chdir("/home/sdt/workspace/lTvsWeb")
            window1 = channel.objects.get(pk=int(2))
            window1.inUse = True
            window1.save()
            print subprocess.Popen("/usr/bin/python hvsInit.py",stdout=subprocess.PIPE, shell=True)
        if request.POST.__contains__("end1")==True and request.POST['end1'] == 'True':
            print "end1"
            # start window 1
            import os
            import subprocess
            os.chdir("/home/sdt/workspace/lTvsWeb")
            window1 = channel.objects.get(pk=int(1))
            window1.inUse = False
            window1.save()
            print subprocess.Popen("/usr/bin/python hvsInit.py",stdout=subprocess.PIPE, shell=True)
        if request.POST.__contains__("end2")==True and request.POST['end2'] == 'True':
            print "end2"
            # start window 1
            import os
            import subprocess
            os.chdir("/home/sdt/workspace/lTvsWeb")
            window2 = channel.objects.get(pk=int(2))
            window2.inUse = False
            window2.save()
            print subprocess.Popen("/usr/bin/python hvsInit.py",stdout=subprocess.PIPE, shell=True)
        if request.POST.__contains__("start3")==True and request.POST['start3'] == 'True':
            print "start3"
            import os
            import subprocess
            os.chdir("C:/deploy/player")
            print  os.system("start /MIN player3.exe")
        if request.POST.__contains__("start4")==True and request.POST['start4'] == 'True':
            print "start4"
            import os
            import subprocess
            os.chdir("C:/deploy/player")
            print  os.system("start /MIN player4.exe")
        if request.POST.__contains__("end3")==True and request.POST['end3'] == 'True':
            print "end3"
            import os
            os.system('taskkill /f /im "player3.exe"')
        if request.POST.__contains__("end4")==True and request.POST['end4'] == 'True':
            print "end4"
            import os
            os.system('taskkill /f /im "player4.exe"')
        if request.POST.__contains__("startDecoder")==True and request.POST['startDecoder'] == 'True':
            print "startDecoder"
            import os
            import subprocess
            os.chdir("C:/Users/Administrator/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup")
            print subprocess.Popen("decoder.bat")
            sleep(1)
            # os.chdir("C:/hvs/")
            # print subprocess.Popen("startDecoder.bat")
        if request.POST.__contains__("endDecoder")==True and request.POST['endDecoder'] == 'True':
            print "endDecoder"
            import os
            os.system('taskkill /f /im "decoder.exe"')
        if request.POST.__contains__("cleanDB")==True and request.POST['cleanDB'] == 'True':
            terminalArray.objects.all().delete()
            channel.objects.all().delete()
            terminal.objects.all().delete()
            userLog.objects.all().delete()
            packetsLostInfo.objects.all().delete()
            packetGrepper.objects.all().delete()
            debugStatus.objects.all().delete()
            userLogInstance = userLog(user= request.user,target=u'系统',content=u'清空数据库')
            userLogInstance.save()

    return render(request,'config/configSystem.html')

@login_required
@csrf_exempt
def logView(request):
    ulList = userLog.objects.order_by('-pk')[0:100]
    debugStatusInstance = debugStatus.objects.get_or_create(pk=1)[0]
    return render(request,'config/log.html',{'ulList':ulList,'debugStatus':debugStatusInstance})

@login_required
@csrf_exempt
def clearUserLog(request):
    userLog.objects.all().delete()
    userLogInstance = userLog(user= request.user,target=u'用户日志',content=u'清除')
    userLogInstance.save()
    return HttpResponse("success")

import csv
@login_required
@csrf_exempt
def exportUserLogAsCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="userLog_%s.csv"' % str(datetime.date.today())
    writer = csv.writer(response)
    writer.writerow([u'操作者'.encode('gb2312'),u'日期'.encode('gb2312'),u'操作对象'.encode('gb2312'),u'动作'.encode('gb2312')])
    for log in userLog.objects.order_by('-pk'):
        writer.writerow([str(log.user).encode('gb2312'),str(log.date).encode('gb2312'),log.target.encode('gb2312'),log.content.encode('gb2312')])
    return response


PORT = 12310
HOST="localhost"
ADDR=(HOST,PORT)

@login_required
@csrf_exempt
def textStyleView(request):
    if request.POST:
        intstanceTextStyle = textStyle.objects.get_or_create(pk=1)[0]
        # print(intstanceTextStyle)
        form = textStyleForm(data = request.POST,instance=intstanceTextStyle)
        if form.is_valid():
            intstance = form.save(commit=True)

            msgToSend = base.hvs_pb2.WrapperMessage()
            msgToSend.textstyle.size = intstance.textSize
            msgToSend.textstyle.location = intstance.location
            msgToSend.textstyle.color = intstance.color
            msgToSend.textstyle.showfps = intstance.showFps
            textStyleContent = msgToSend.SerializeToString()
            try:
                tcpCliSock = socket(AF_INET,SOCK_STREAM)
                tcpCliSock.connect(ADDR)
                tcpCliSock.send(textStyleContent)
                tcpCliSock.close()
            except Exception as e:
                print(e)

            return HttpResponseRedirect("/sdt-hts/textStyle/")
        else:
            print(form)
            return render(request,'config/textStyle.html',{'form':form})
    else:
        intstanceTextStyle = textStyle.objects.get_or_create(pk=1)[0]
        form = textStyleForm(instance=intstanceTextStyle)
        # print(form)
        return render(request,'config/textStyle.html',{'form':form})
