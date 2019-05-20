# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render

# # Create your views here.


# @login_required
# def homeView(request):
# 	return render(request,'base.html')



# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseServerError
from base.models import *
from config.models import *
from base.forms import *
import json,os,re
import csv
from time import sleep,ctime
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from socket import *
import hvs_pb2
# 检查显示器信息函数1
# 输入：None
# 输出：显示器列表,并关联数据库
# 格式：[ ['id','name','pix'], [...] , [...] ]
# def checkMonitor():
# 	r = os.system("MonitorInfoView.exe /HideInactiveMonitors 1 /scomma monitor.csv")
# 	if r == 0:
# 		if os.path.exists("./monitor.csv"):
# 			reader = csv.reader(open("monitor.csv"),delimiter=",")
# 		else:
# 			return False
# 		ret = []
# 		print "-----------------------"
# 		for line in reader:
# 			print line[0]
# 			print line[5]
# 			print "-----------------------"
# 	return True

@login_required
def homeView(request):
	return render(request,'base/index.html')


def promptForTerminalList(arrayProto,terminalList):
	pass

myterminalArray = hvs_pb2.TerminalArray()
# HOST = "192.168.1.120"
HOST = "localhost"
PORT=12310
BUFSIZ=10024

@login_required
def index(request):
	return render(request,'base/index.html')

def log_me_out(request):
    # logout the user
    logout(request)
    return HttpResponseRedirect('/sdt-hts/')

from django.core import serializers

@login_required
def configChannels(request):
	if request.POST:
		form = channelForm(request.POST)
		if form.is_valid():
			print "form.is_valid"
			channelInstance = form.save(commit=False)
			channelInstance.saperateNumber = 4;
			channelInstance.pos=""
			channelInstance.save()
			channels = channel.objects.filter(active = True)
			try:
				tcpCliSock = socket(AF_INET,SOCK_STREAM)
				tcpCliSock.connect(ADDR)
				# PromptForAddress(channellist.channel.add(),channelInstance)
				# data = channellist.SerializeToString()
				# tcpCliSock.send(data)
				tcpCliSock.close()
			except Exception, e:
				print "socket&connect&send with error:",e
			return render(request,'base/configChannels.html',{'ChannelForm':form,'msg':"success"})
		else:
			print "form.is not valid"
			return render(request,'base/configChannels.html',{'ChannelForm':form,'msg':"error"})
		# print "post"
		# if request.is_ajax():
		# 	print "ajax post"

		# form = channelForm(request.POST)

		# if form.is_valid():
		# 	print "form.is_valid"
		# 	channelInstance = form.save(commit=True)
		# 	channelInstance.save()
		# 	channels = channel.objects.all()
		# 	try:
		# 		tcpCliSock = socket(AF_INET,SOCK_STREAM)
		# 		tcpCliSock.connect(ADDR)
		# 		PromptForAddress(channellist.channel.add(),channelInstance)
		# 		data = channellist.SerializeToString()
		# 		tcpCliSock.send(data)
		# 		tcpCliSock.close()
		# 	except Exception, e:
		# 		print "socket&connect&send with error:",e
		# 	return render(request,'base/configChannels.html',{'ChannelForm':form,'channels':channels})
		# else:
		# 	print "form.is not valid"
		# 	try:
		# 		if form['name'].value() == "":
		# 			raise Exception(u"请输入有效的通道名称")
		# 		elif form['saperateNumber'].value() == "":
		# 			raise Exception(u"请输入有效的通道数量")
		# 	except Exception,e:
		# 		return HttpResponseServerError(e)
		# 	print form.name.errors
		# 	return HttpResponseServerError(str("errors"))
		# 	channels = channel.objects.all()
		# 	return render(request,'base/configChannels.html',{'ChannelForm':form,'channels':channels})
	elif request.GET:

		try:
			###################
			# ljq
			channelList = channel.objects.filter(active = True)
			# channelList = channel.objects.all()
			###################

			json_reply = serializers.serialize("json",channelList)

			return HttpResponse(json_reply)

		except Exception as e:

			return HttpResponseServerError(e.strerror)
	form = channelForm()
	channels = channel.objects.all()
	return render(request,'base/configChannels.html',{'ChannelForm':form,'channels':channels})

@login_required
def addTerminals(request):
	if request.POST:
		form = terminalForm(request.POST)
		errorContent=""
		if terminal.objects.count()>=21:
			form.add_error(None,'zzzzzz')
			print ">20"
			errorContent = u"已达到最大终端数20"
			return render(request,'base/addTerminals.html',{'terminalForm':form,'msg':"error",'content':errorContent})
		if form.is_valid():
			terminalInstance = form.save(commit=False)
			terminalInstance.save()
			uL = userLog(user=request.user,target=terminalInstance.name,content=u"添加")
			uL.save()
			for i in range(1,21):
				item = terminalArray.objects.get_or_create(pk=i)[0]
				if item.status == False:
					item.ip = terminalInstance.terminalIP
					item.name = terminalInstance.name
					item.status = True
					item.save()
					break
			######
			WrapperMessageTa = hvs_pb2.WrapperMessage()
			for i in range(1,21):
				t = terminalArray.objects.get_or_create(pk=i)[0]
				temp = WrapperMessageTa.ta.terminal.add()
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
			# 发给主程序
			errorlist = []
			try:
				PORT = 12310
				print "port is ",PORT
				ADDR=(HOST,PORT)
				tcpCliSock = socket(AF_INET,SOCK_STREAM)
				tcpCliSock.connect(ADDR)
				typedata = WrapperMessageTa.SerializeToString()
				tcpCliSock.send(typedata)
				tcpCliSock.close()
			except Exception as e:
				print "send main C++ error",e
				errorlist.append(e)
			# 发给抓包服务器
			# try:
			# 	pgInstance = packetGrepper.objects.get_or_create(pk=1)[0]
			# 	if pgInstance.active == True:
			# 		PGHOST = pgInstance.ip
			# 		PORT = 12315
			# 		print "send packet grepper ip is %s port is %s"% (PGHOST,PORT)
			# 		ADDR=(PGHOST,PORT)
			# 		tcpCliSock = socket(AF_INET,SOCK_STREAM)
			# 		tcpCliSock.connect(ADDR)
			# 		typedata = WrapperMessageTa.SerializeToString()
			# 		tcpCliSock.send(typedata)
			# 		tcpCliSock.close()
			# except Exception as e1:
			# 	print "send main C++ error",e1
			# 	errorlist.append(e1)
			# 发给每个屏幕
			#################
			# ljq
			for screen in channel.objects.filter(active=True):
			# for screen in channel.objects.all():
			#################
				try:
					PORT = 12315+int(screen.pk)
					print "screen port is ",PORT
					ADDR=(HOST,PORT)
					tcpCliSock = socket(AF_INET,SOCK_STREAM)
					tcpCliSock.connect(ADDR)
					print "WuNL"
					print WrapperMessageTa
					taToSend = WrapperMessageTa.SerializeToString()
					tcpCliSock.send(taToSend)
					tcpCliSock.close()
				except Exception as e2:
					print "send screen id %d error"%int(screen.pk),e2
					errorlist.append(e2)
			form = terminalForm()
			if len(errorlist)!=0:
				print errorlist,len(errorlist)
				errorcontent = u"保存成功，但存在网络错误"
			else:
				errorcontent = u"保存成功"
			return render(request,'base/addTerminals.html',{'terminalForm':form,'msg':"success",'content':errorcontent})
		else:
			errorContent=u"输入错误"
			print "form.is not valid"
			return render(request,'base/addTerminals.html',{'terminalForm':form,'msg':"error",'content':errorContent})
	elif request.GET:
		try:
			terminalList = terminal.objects.all()
			json_reply = serializers.serialize("json",terminalList)
			return HttpResponse(json_reply)
		except Exception as e:
			return HttpResponseServerError(e.strerror)
	else:
		# nowStatus = registerStatus.objects.get(pk=1).resgisterStatus
		# print nowStatus
		# if nowStatus==False:
		# 	return HttpResponseRedirect("/sdt-hts/license/")
		form = terminalForm()
		return render(request,'base/addTerminals.html',{'terminalForm':form})

@login_required
@csrf_exempt
def editTerminals(request,terminalID):
	print " --------------into editTerminals view --------------------with id %s" % terminalID

	if request.POST:
		tid = int(terminalID)
		curTerminal = terminal.objects.get(pk=tid)
		curTerminalInArray = terminalArray.objects.get(ip = curTerminal.terminalIP)
		form = terminalForm(data = request.POST,instance = curTerminal)
		if form.is_valid():
			print "edit form is valid"
			newTerminal = form.save()
			uL = userLog(user=request.user,target=curTerminalInArray.name,content=u"修改为%s,IP:%s" % (newTerminal.name,newTerminal.terminalIP))
			uL.save()
			curTerminalInArray.ip = newTerminal.terminalIP
			curTerminalInArray.name = newTerminal.name
			curTerminalInArray.status = True
			curTerminalInArray.save()
			######
			WrapperMessageTa = hvs_pb2.WrapperMessage()

			for i in range(1,21):
				t = terminalArray.objects.get(pk=i)
				temp = WrapperMessageTa.ta.terminal.add()
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
			# 发给主程序
			try:
				PORT = 12310
				print "port is ",PORT
				ADDR=(HOST,PORT)
				tcpCliSock = socket(AF_INET,SOCK_STREAM)
				tcpCliSock.connect(ADDR)
				typedata = WrapperMessageTa.SerializeToString()
				tcpCliSock.send(typedata)
				tcpCliSock.close()
			except Exception as e:
				print "send main C++ error",e
			# 发给抓包服务器
			# try:
			# 	pgInstance = packetGrepper.objects.get_or_create(pk=1)[0]
			# 	if pgInstance.active == True:
			# 		PGHOST = pgInstance.ip
			# 		PORT = 12315
			# 		print "send packet grepper ip is %s port is %s"% (PGHOST,PORT)
			# 		ADDR=(PGHOST,PORT)
			# 		tcpCliSock = socket(AF_INET,SOCK_STREAM)
			# 		tcpCliSock.connect(ADDR)
			# 		typedata = WrapperMessageTa.SerializeToString()
			# 		tcpCliSock.send(typedata)
			# 		tcpCliSock.close()
			# except Exception as e1:
			# 	print "send main C++ error",e1
			# 发给每个屏幕
			for screen in channel.objects.filter(active=True):
				try:
					PORT = 12315+int(screen.pk)
					print "screen port is ",PORT
					ADDR=(HOST,PORT)
					tcpCliSock = socket(AF_INET,SOCK_STREAM)
					tcpCliSock.connect(ADDR)
					taToSend = WrapperMessageTa.SerializeToString()
					tcpCliSock.send(taToSend)
					tcpCliSock.close()
				except Exception as e:
					print "send screen id %d error"%int(screen.pk),e

			form = terminalForm()
			return render(request,'base/addTerminals.html',{'terminalForm':form,'msg':'修改成功'})
		return render(request,'base/editTerminals.html',{'terminalForm':form,'terminalID':tid,'msg':'error','content':'修改失败！'})
	else:
		tid = int(terminalID)
		curTerminal = terminal.objects.get(pk=tid)
		curTerminalInArray = terminalArray.objects.get(ip = curTerminal.terminalIP)
		form = terminalForm(instance = curTerminal)
		return render(request,'base/editTerminals.html',{'terminalForm':form,'terminalID':tid})

@login_required
@csrf_exempt
def deleteTerminal(request,terminalID):
	print "------------------into deleteTerminal-----------------with id:",terminalID
	if request.method == 'DELETE':
		print "delete DELETE"
		try:
			tid = int(terminalID)
			tml = terminal.objects.get(pk=tid)
			try:
				tmlInArray = terminalArray.objects.get(ip = tml.terminalIP)
			except terminalArray.DoesNotExist:
				tml.delete()
				return HttpResponse(u"数据库错误")

			for chanl in channel.objects.all():
				# 1:1,16,16,1, 2:2,16, 3:3, 4:16, 5:12, 6:16,16,16,16, 7:10,1, 8:16, 9:15,7,13, 10:16,16,16, 11:16, 12:16, 13:16,16, 14:15,11, 15:16, 16:16,16,

				# 删除所有:|,d+,
				superClip = "(?<=:|,)"+str(tmlInArray.pk)+','+"(?=\d| |$)"
				# 修复 1: 2: 这种情况
				superClip1 = ":"+"(?= |$)"
				# 去结尾
				superClip2 = "(?<=:)"+str(tmlInArray.pk)+",$"
				# superClip3 = "(?<=,)"+str(tmlInArray.pk)+",$"
				# clip2 = "(?<=:)"+str(tmlInArray.pk)+',$'
				if chanl.pollingPos != None:
					mycurrentPos = re.subn(superClip,'',str(chanl.pollingPos))[0]

					mycurrentPos = re.subn(superClip1,':-1,',mycurrentPos)[0]

					mycurrentPos = re.subn(superClip2,'-1,',mycurrentPos)[0]

					chanl.pollingPos = mycurrentPos
					chanl.save()
			tmlInArray.ip=""
			tmlInArray.name = ""
			tmlInArray.status = False
			tmlInArray.save()
			tml.delete()
			uL = userLog(user=request.user,target=tml.name,content=u"删除")
			uL.save()
			######
			WrapperMessageTa = hvs_pb2.WrapperMessage()

			for i in range(1,21):
				t = terminalArray.objects.get(pk=i)
				temp = WrapperMessageTa.ta.terminal.add()
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
			# print WrapperMessageTa
			PORT = 12310
			print "port is ",PORT
			ADDR=(HOST,PORT)
			tcpCliSock = socket(AF_INET,SOCK_STREAM)
			tcpCliSock.connect(ADDR)
			typedata = WrapperMessageTa.SerializeToString()
			tcpCliSock.send(typedata)

			# 发给抓包服务器
			# try:
			# 	pgInstance = packetGrepper.objects.get_or_create(pk=1)[0]
			# 	if pgInstance.active == True:
			# 		PGHOST = pgInstance.ip
			# 		PORT = 12315
			# 		print "send packet grepper ip is %s port is %s"% (PGHOST,PORT)
			# 		ADDR=(PGHOST,PORT)
			# 		tcpCliSock = socket(AF_INET,SOCK_STREAM)
			# 		tcpCliSock.connect(ADDR)
			# 		typedata = WrapperMessageTa.SerializeToString()
			# 		tcpCliSock.send(typedata)
			# 		tcpCliSock.close()
			# except Exception as e:
			# 	print "send packet grepper error",e
			for screen in channel.objects.filter(active=True):
				try:
					# print "delete screen content:",screen.pk,screen.pollingPos
					msgToSend = hvs_pb2.WrapperMessage()

					msgToSend.cpl.id = int(screen.pk)
					msgToSend.cpl.saperateNumber = int(screen.saperateNumber)
					msgToSend.cpl.style = 1
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

					PORT = 12315+int(screen.pk)
					print "port is ",PORT
					ADDR=(HOST,PORT)
					tcpCliSock = socket(AF_INET,SOCK_STREAM)
					tcpCliSock.connect(ADDR)

					taToSend = WrapperMessageTa.SerializeToString()
					tcpCliSock.send(taToSend)

					typedata = msgToSend.SerializeToString()
					tcpCliSock.send(typedata)
					tcpCliSock.close()
				except Exception as e2:
					print "send screen id %d error"%int(screen.pk),e2
			return HttpResponse(u"删除成功")
		except Exception,e:
			ttt = HttpResponseServerError(e)

			return HttpResponse(e)
	else:
		return HttpResponse(u"未知错误")


def modifyArray(posList):
	if terminalArray.objects.count()>20:
		return False

import re

def getSaperateScreen(request,saperateNum,screenID):
	print "**************into getSaperateScreen Fun***************"
	terminalList = terminalArray.objects.filter(status = True)
	curChannel = channel.objects.get(pk=screenID)
	if curChannel.pos == None:
		curChannel.pos = ""
		curChannel.save()
	pos = curChannel.pos
	posList = pos.split(" ")
	dstList = []
	for i in range(saperateNum):
		dstList.append([0,0])
	for curpos in posList:
		paramList = curpos.split("-")
		for i in range(saperateNum):
			if paramList[0] == str(i+1):
				dstList[i][0] =  (paramList[1])
				dstList[i][1] = terminalList.get(pk=int(paramList[1])).name
	# 需要发送数据到C++
	if curChannel.saperateNumber != saperateNum:
		curChannel.saperateNumber = saperateNum;
		curChannel.save()
		try:
			msgtype = hvs_pb2.MsgType()
			msgtype.msgtype = hvs_pb2.MsgType.POLLINGCONTENT
			cn = hvs_pb2.ChannelPolling()
			cn.id = 1
			cn.style = 1
			cn.saperateNumber = curChannel.saperateNumber
			cn.pollingTime = curChannel.pollingTime
			cn.isPolling = False
			curChannel.polling	= False
			curChannel.save()
			dstArray = []
			for i in range(4):
				dstArray.append(-1)

			pos = curChannel.pos
			posList = pos.split(" ")
			for curpos in posList:
				paramList = curpos.split("-")
				for i in range(saperateNum):
					if paramList[0] == str(i+1):
						dstArray[i] =  terminalList.get(pk=int(paramList[1])).pk

			for j in range(curChannel.saperateNumber):
				cn.terminalID.append(str(dstArray[j]))

			tcpCliSock = socket(AF_INET,SOCK_STREAM)
			tcpCliSock.connect(ADDR)
			typedata = msgtype.SerializeToString()
			tcpCliSock.send(typedata)
			sleep(0.2)
			data = cn.SerializeToString()
			tcpCliSock.send(data)
			tcpCliSock.close()
		except Exception, e:
			print "socket&connect&send with error:",e
	tmpurl = 'base/configChannel'+str(saperateNum)+'.html'
	return render(tmpurl,{'terminals':terminalList,'channelID':screenID,'dstList':dstList})

@login_required
@csrf_exempt
def configChannelWithNum(request,channelID,channelNum):
	if request.method == 'POST':
		try:
			channelNum = int(channelNum)
		except Exception,e:
			print e
		if channelNum == 1:
			var = request.POST.get('value1')
			curChannel = channel.objects.get(pk=channelID)


			if var=="null":
				var=""
				if curChannel.pos != None:
					clip = str(1)+'\-\d+'
					currentPos = re.sub(clip,'',curChannel.pos)
					curChannel.pos = currentPos
				else:
					curChannel.pos=""
				curChannel.pos = curChannel.pos.lstrip()
				curChannel.pos = curChannel.pos.rstrip()
				curChannel.save()
			else:
				clip = str(1)+'\-\d+'
				if curChannel.pos != None:
					try:
						currentPos = re.sub(clip,'',str(curChannel.pos))
						curChannel.pos = currentPos
						currentPos = ' '+str(1)+'-'+str(var)
						curChannel.pos += currentPos
					except Exception,e:
						print e
						currentPos = ' '+str(1)+'-'+str(var)
						curChannel.pos += currentPos
				else:
					currentPos = ' '+str(1)+'-'+str(var)
					curChannel.pos = currentPos

				curChannel.pos = curChannel.pos.lstrip()
				curChannel.pos = curChannel.pos.rstrip()
				curChannel.save()

			return HttpResponse("recv post with 1")
		elif channelNum == 4:
			var1 = request.POST.get('value1')
			var2 = request.POST.get('value2')
			var3 = request.POST.get('value3')
			var4 = request.POST.get('value4')
			print var1,var2,var3,var4
			curChannel = channel.objects.get(pk=channelID)
			i = 1
			for var in [var1,var2,var3,var4]:
				# 如果该小分屏上没有配终端，将以前数据清空
				if var=="null":
					var=""
					if curChannel.pos != None:
						clip = str(i)+'\-\d+'
						currentPos = re.sub(clip,'',curChannel.pos)
						curChannel.pos = currentPos
					else:
						curChannel.pos=""
					curChannel.pos = curChannel.pos.lstrip()
					curChannel.pos = curChannel.pos.rstrip()
					curChannel.save()

				# 用户在该小分屏上配了终端，先清空再写入最新的
				else:
					clip = str(i)+'\-\d+'
					if curChannel.pos != None:
						try:
							currentPos = re.sub(clip,'',str(curChannel.pos))
							curChannel.pos = currentPos
							currentPos = ' '+str(i)+'-'+str(var)
							curChannel.pos += currentPos
						except Exception,e:
							print e
							currentPos = ' '+str(i)+'-'+str(var)
							curChannel.pos += currentPos
					else:
						currentPos = ' '+str(i)+'-'+str(var)
						curChannel.pos = currentPos

					curChannel.pos = curChannel.pos.lstrip()
					curChannel.pos = curChannel.pos.rstrip()
					curChannel.save()

				i=i+1
			try:
				cn = hvs_pb2.ChannelPolling()
				cn.id = 1
				cn.style = 1
				cn.saperateNumber = curChannel.saperateNumber
				cn.pollingTime = curChannel.pollingTime
				cn.isPolling = False
				curChannel.polling	= False
				curChannel.save()
				dstArray = []
				for i in range(4):
					dstArray.append(-1)

				pos = curChannel.pos
				posList = pos.split(" ")
				for curpos in posList:
					paramList = curpos.split("-")
					if paramList[0]==u'1':
						tip = terminal.objects.get(pk=int(paramList[1])).terminalIP
						dstArray[0] =  terminalArray.objects.get(ip = tip).pk
					if paramList[0]==u'2':
						tip = terminal.objects.get(pk=int(paramList[1])).terminalIP
						dstArray[1] =  terminalArray.objects.get(ip = tip).pk
					if paramList[0]==u'3':
						tip = terminal.objects.get(pk=int(paramList[1])).terminalIP
						dstArray[2] =  terminalArray.objects.get(ip = tip).pk
					if paramList[0]==u'4':
						tip = terminal.objects.get(pk=int(paramList[1])).terminalIP
						dstArray[3] =  terminalArray.objects.get(ip = tip).pk
				for j in range(curChannel.saperateNumber):
					cn.terminalID.append(str(dstArray[j]))

				tcpCliSock = socket(AF_INET,SOCK_STREAM)
				tcpCliSock.connect(ADDR)
				typedata = msgtype.SerializeToString()
				tcpCliSock.send(typedata)
				sleep(0.2)
				data = cn.SerializeToString()
				tcpCliSock.send(data)
				tcpCliSock.close()
			except Exception, e:
				print "socket&connect&send with error:",e
			return HttpResponse("recv post with 4")


	try:
		channelNum = int(channelNum)
	except Exception,e:
		print e
		return render(request,'base/index.html')
	terminalList = terminal.objects.all()
	if channelNum == 1:
		return getSaperateScreen(request,1,channelID)
	elif channelNum == 4:
		return getSaperateScreen(request,4,channelID)
	elif channelNum == 9:
		return getSaperateScreen(request,9,channelID)
	elif channelNum == 16:
		return getSaperateScreen(request,16,channelID)
	else:
		return render(request,'base/configChannel.html',{'terminals':terminalList,'channelID':channelID})
@login_required
def configChannel(request,channelID):

	terminalList = terminal.objects.all()
	return render(request,'base/configChannel.html',{'terminals':terminalList,'channelID':channelID})


def getPollingWithNum(request,pollingNum,screenID):
	print "getPollingWithNum ",pollingNum
	dstList = []
	for i in range(pollingNum):
		dstList.append([])
	print len(dstList)
	terminalList = terminalArray.objects.filter(status = True)
	curChannel = channel.objects.get(pk=screenID)
	# return HttpResponse("recv post with getPollingWithNum")
	if curChannel.pollingPos == None:
		curChannel.pollingPos = ""
		curChannel.save()
	curPollingPos = curChannel.pollingPos
	posList = curPollingPos.split(" ")
	print posList
	# 1:1,2,3,4,
	i = 1
	finalPosListWithName = []
	for posInSingleScreen in posList:
		if i <= pollingNum:
			tempList = []
			clip = "^"+str(i)+":.+,$"
			if len(re.findall(clip,posInSingleScreen)) != 0:
				# 去掉如 1: 2:
				newPosInSingleScreen = re.sub(str(i)+":",'',posInSingleScreen)

				newPosInSingleScreen = re.sub(",$",'',newPosInSingleScreen)
				finalPosList = newPosInSingleScreen.split(",")
				for item in finalPosList:
					if item != u"-1":
						name = terminalList.get(pk = int(item)).name
						tempList.append([item,name])
					else:
						tempList.append([-1,-1])
				dstList[int(i-1)] = finalPosList
			i +=1
		else:
			break
		finalPosListWithName.append(tempList)

	print finalPosListWithName

	# 如果分屏数发生变化则向电视墙发送数据
	if (curChannel.saperateNumber != int(pollingNum)):
		# curChannel.saperateNumber = int(pollingNum)
		# curChannel.save()
		print "ready to send data!"
		try:
			msgtype = hvs_pb2.MsgType()
			msgtype.msgtype = hvs_pb2.MsgType.POLLINGCONTENT
			cn = hvs_pb2.ChannelPolling()
			cn.id = 1
			cn.style = 1
			cn.saperateNumber = curChannel.saperateNumber
			cn.pollingTime = curChannel.pollingTime
			cn.isPolling = curChannel.polling
			dstArray = []
			for i in range(pollingNum):
				dstArray.append("-1")

			pos = curChannel.pollingPos
			posList = pos.split(" ")

			for curpos in posList:
				paramList = curpos.split(":")
				for i in range(1,pollingNum+1):
					if str(i) == paramList[0]:
						posListInSingleScreen = re.sub(',',' ',paramList[1])
						dstArray[int(i-1)] = posListInSingleScreen
			for item in dstArray:
				cn.terminalID.append(str(item))
			# tcpCliSock = socket(AF_INET,SOCK_STREAM)
			# tcpCliSock.connect(ADDR)
			# typedata = msgtype.SerializeToString()
			# tcpCliSock.send(typedata)
			# sleep(0.2)
			# data = cn.SerializeToString()
			# tcpCliSock.send(data)
			# tcpCliSock.close()
		except Exception, e:
			print "socket&connect&send with error:",e
	if pollingNum == 1:
		return render(request,'base/configPolling1.html',{'terminals':terminalList,'curChannel':curChannel,'channelID':screenID,'dstList':finalPosListWithName})
	if pollingNum == 2:
		return render(request,'base/configPolling2.html',{'terminals':terminalList,'curChannel':curChannel,'channelID':screenID,'dstList':finalPosListWithName})
	if pollingNum == 3:
		return render(request,'base/configPolling3.html',{'terminals':terminalList,'curChannel':curChannel,'channelID':screenID,'dstList':finalPosListWithName})
	if pollingNum == 4:
		return render(request,'base/configPolling4.html',{'terminals':terminalList,'curChannel':curChannel,'channelID':screenID,'dstList':finalPosListWithName})
	if pollingNum == 6:
		return render(request,'base/configPolling6.html',{'terminals':terminalList,'curChannel':curChannel,'channelID':screenID,'dstList':finalPosListWithName})
	if pollingNum == 9:
		return render(request,'base/configPolling9.html',{'terminals':terminalList,'curChannel':curChannel,'channelID':screenID,'dstList':finalPosListWithName})
	if pollingNum == 16:
		return render(request,'base/configPolling16.html',{'terminals':terminalList,'curChannel':curChannel,'channelID':screenID,'dstList':finalPosListWithName})
	if pollingNum == 20:
		return render(request,'base/configPolling20.html',{'terminals':terminalList,'curChannel':curChannel,'channelID':screenID,'dstList':finalPosListWithName})

def postPollingWithNum(request,pollingNum,screenID):
	# *******************************************************************************************************************
	# 轮巡

	print "configPolling " +str(pollingNum)
	terminalList = terminalArray.objects.filter(status = True)
	curChannel = channel.objects.get(pk=screenID)
	# var1,var2,var3,var4,var5,var6,var7,var8,var9,var10,var11,var12,var13,var14,var15,var16=""
	var1=var2=var3=var4=var5=var6=var7=var8=var9=var10=var11=var12=var13=var14=var15=var16=var17=var18=var19=var20=""
	if pollingNum==1:
		var1 = request.POST.getlist("var1[]")
	if pollingNum==2:
		var1 = request.POST.getlist("var1[]")
		var2 = request.POST.getlist("var2[]")
	if pollingNum==3:
		var1 = request.POST.getlist("var1[]")
		var2 = request.POST.getlist("var2[]")
		var3 = request.POST.getlist("var3[]")
	if pollingNum==4:
		var1 = request.POST.getlist("var1[]")
		var2 = request.POST.getlist("var2[]")
		var3 = request.POST.getlist("var3[]")
		var4 = request.POST.getlist("var4[]")
	if pollingNum==6:
		var1 = request.POST.getlist("var1[]")
		var2 = request.POST.getlist("var2[]")
		var3 = request.POST.getlist("var3[]")
		var4 = request.POST.getlist("var4[]")
		var5 = request.POST.getlist("var5[]")
		var6 = request.POST.getlist("var6[]")
	if pollingNum==9:
		var1 = request.POST.getlist("var1[]")
		var2 = request.POST.getlist("var2[]")
		var3 = request.POST.getlist("var3[]")
		var4 = request.POST.getlist("var4[]")
		var5 = request.POST.getlist("var5[]")
		var6 = request.POST.getlist("var6[]")
		var7 = request.POST.getlist("var7[]")
		var8 = request.POST.getlist("var8[]")
		var9 = request.POST.getlist("var9[]")
	if pollingNum==16:
		var1 = request.POST.getlist("var1[]")
		var2 = request.POST.getlist("var2[]")
		var3 = request.POST.getlist("var3[]")
		var4 = request.POST.getlist("var4[]")
		var5 = request.POST.getlist("var5[]")
		var6 = request.POST.getlist("var6[]")
		var7 = request.POST.getlist("var7[]")
		var8 = request.POST.getlist("var8[]")
		var9 = request.POST.getlist("var9[]")
		var10 = request.POST.getlist("var10[]")
		var11 = request.POST.getlist("var11[]")
		var12 = request.POST.getlist("var12[]")
		var13 = request.POST.getlist("var13[]")
		var14 = request.POST.getlist("var14[]")
		var15 = request.POST.getlist("var15[]")
		var16 = request.POST.getlist("var16[]")
	if pollingNum==20:
		var1 = request.POST.getlist("var1[]")
		var2 = request.POST.getlist("var2[]")
		var3 = request.POST.getlist("var3[]")
		var4 = request.POST.getlist("var4[]")
		var5 = request.POST.getlist("var5[]")
		var6 = request.POST.getlist("var6[]")
		var7 = request.POST.getlist("var7[]")
		var8 = request.POST.getlist("var8[]")
		var9 = request.POST.getlist("var9[]")
		var10 = request.POST.getlist("var10[]")
		var11 = request.POST.getlist("var11[]")
		var12 = request.POST.getlist("var12[]")
		var13 = request.POST.getlist("var13[]")
		var14 = request.POST.getlist("var14[]")
		var15 = request.POST.getlist("var15[]")
		var16 = request.POST.getlist("var16[]")
		var17 = request.POST.getlist("var17[]")
		var18 = request.POST.getlist("var18[]")
		var19 = request.POST.getlist("var19[]")
		var20 = request.POST.getlist("var20[]")
	isPolling = request.POST.get("isPolling")
	pollingTime = request.POST.get("pollingTime")

	# 目标 轮巡POS格式 1:1,2,3,4 2:,1,2,3,4 3:20,11,12 ....
	pollingPos = curChannel.pollingPos
	posBytesToSave = ["1:-1,","2:-1,","3:-1,","4:-1,","5:-1,","6:-1,","7:-1,","8:-1,","9:-1,","10:-1,","11:-1,","12:-1,","13:-1,","14:-1,","15:-1,","16:-1,","17:-1,","18:-1,","19:-1,","20:-1,"]
	if pollingPos == "":
			for i in range(0,20):
				pollingPos += posBytesToSave[i]+" "
	curChannel.pollingPos = pollingPos
	curChannel.save()
	posBytesToSend = []
	for i in range(0,pollingNum):
		posBytesToSend.append("")

	i=0
	tmpList = [var1,var2,var3,var4,var5,var6,var7,var8,var9,var10,var11,var12,var13,var14,var15,var16,var17,var18,var19,var20]
	for var in tmpList[0:pollingNum]:

		if len(var)!=0:
			for tid in var:
				if terminalArray.objects.filter(pk = int(tid)).filter(status=True).count() == 0:
					return HttpResponse(u"终端不存在，请刷新后重试")
				posBytesToSend[i] += (str(tid)+" ")
				posBytesToSave[i] = re.sub("-1,","",posBytesToSave[i])
				posBytesToSave[i] += (str(tid)+",")
		else:
			posBytesToSend[i] = "-1"
		i = i+1

	# 存数据到数据库
	try:
		curChannel.saperateNumber = int(pollingNum)
		curChannel.save()
		if isPolling == "true":

			curChannel.polling = True
		else:
			curChannel.polling = False
		if pollingPos != None:
			posList = pollingPos.split(" ")
		else:
			pollingPos = ""
			posList = []
		pollingPos = pollingPos.lstrip()
		pollingPos = pollingPos.rstrip()

		# 不是第一次运行，存有历史数据。先用正则表达式清空数据，再将新数据写入

		for i in range(1,pollingNum+1):
			if i == 1:
				clip = "^"+str(i)+":-?(\d{1,10000},){1,10000}"
				# print "bef:",pollingPos
				# print clip,posBytesToSave[i-1]
				pollingPos = re.sub(clip,posBytesToSave[i-1],pollingPos)
				# print "aft:",pollingPos
			clip = " "+str(i)+":-?(\d{1,10000},){1,10000}"
			# print "bef:",pollingPos
			# print clip,posBytesToSave[i-1]
			pollingPos = re.sub(clip," "+posBytesToSave[i-1],pollingPos)
			# print "aft:",pollingPos
			# for pos in posBytesToSave:
			# 	pollingPos += (pos+" ")
		pollingPos = pollingPos.lstrip()
		pollingPos = pollingPos.rstrip()
		curChannel.pollingPos = pollingPos
		curChannel.pollingTime = pollingTime
		curChannel.save()

		userLogInstance = userLog(user= request.user,target=u'轮询',content=u'修改%s轮询内容' % curChannel.name)
		userLogInstance.save()
		print "final posPolling:",curChannel.pollingPos
	except Exception, e:
		print "save database error:",e
	# 发送数据
	try:
		msgToSend = hvs_pb2.WrapperMessage()
		msgToSend.cpl.id = int(screenID)
		msgToSend.cpl.active = True
		msgToSend.cpl.inuse = curChannel.inUse
		msgToSend.cpl.saperateNumber = int(pollingNum)
		if int(pollingNum) == 20:
			msgToSend.cpl.style = 3
		else:
			msgToSend.cpl.style = 1
		msgToSend.cpl.pollingTime = int(pollingTime)
		msgToSend.cpl.isPolling = curChannel.polling

		for item in posBytesToSend:
			msgToSend.cpl.terminalID.append(item)
		pollingContent = msgToSend.SerializeToString()
		PORT = 12310
		print "port is ",PORT
		print "msgToSend: ", msgToSend

		ADDR=(HOST,PORT)
		tcpCliSock = socket(AF_INET,SOCK_STREAM)
		tcpCliSock.connect(ADDR)
		print tcpCliSock.send(pollingContent)
		tcpCliSock.close()

	except Exception, e:
		print "socket&connect&send with error:",e
		return HttpResponse(u"连接电视墙显示程序%d失败!"%int(screenID))
	return HttpResponse("success")

# 检测提交的视频通道数据中，是否存在重复项：包含自身重复，与其他大屏的数据重复
# 不重复则判断状态正常，返回True
# 重复返回False
def checkPostDate(request,screenID,pollingNum):
	terminalList = terminalArray.objects.filter(status = True)
	curChannel = channel.objects.get(pk=screenID)
	pollingNum = int(pollingNum)
	# var1,var2,var3,var4,var5,var6,var7,var8,var9,var10,var11,var12,var13,var14,var15,var16=""
	var1=var2=var3=var4=var5=var6=var7=var8=var9=var10=var11=var12=var13=var14=var15=var16=""
	if pollingNum==1:
		var1 = request.POST.getlist("var1[]")
	if pollingNum==2:
		var1 = request.POST.getlist("var1[]")
		var2 = request.POST.getlist("var2[]")
	if pollingNum==3:
		var1 = request.POST.getlist("var1[]")
		var2 = request.POST.getlist("var2[]")
		var3 = request.POST.getlist("var3[]")
	if pollingNum==4:
		var1 = request.POST.getlist("var1[]")
		var2 = request.POST.getlist("var2[]")
		var3 = request.POST.getlist("var3[]")
		var4 = request.POST.getlist("var4[]")
	if pollingNum==6:
		var1 = request.POST.getlist("var1[]")
		var2 = request.POST.getlist("var2[]")
		var3 = request.POST.getlist("var3[]")
		var4 = request.POST.getlist("var4[]")
		var5 = request.POST.getlist("var5[]")
		var6 = request.POST.getlist("var6[]")
	if pollingNum==9:
		var1 = request.POST.getlist("var1[]")
		var2 = request.POST.getlist("var2[]")
		var3 = request.POST.getlist("var3[]")
		var4 = request.POST.getlist("var4[]")
		var5 = request.POST.getlist("var5[]")
		var6 = request.POST.getlist("var6[]")
		var7 = request.POST.getlist("var7[]")
		var8 = request.POST.getlist("var8[]")
		var9 = request.POST.getlist("var9[]")
	if pollingNum==16:
		var1 = request.POST.getlist("var1[]")
		var2 = request.POST.getlist("var2[]")
		var3 = request.POST.getlist("var3[]")
		var4 = request.POST.getlist("var4[]")
		var5 = request.POST.getlist("var5[]")
		var6 = request.POST.getlist("var6[]")
		var7 = request.POST.getlist("var7[]")
		var8 = request.POST.getlist("var8[]")
		var9 = request.POST.getlist("var9[]")
		var10 = request.POST.getlist("var10[]")
		var11 = request.POST.getlist("var11[]")
		var12 = request.POST.getlist("var12[]")
		var13 = request.POST.getlist("var13[]")
		var14 = request.POST.getlist("var14[]")
		var15 = request.POST.getlist("var15[]")
		var16 = request.POST.getlist("var16[]")
	isPolling = request.POST.get("isPolling")
	pollingTime = request.POST.get("pollingTime")

	tmpList = [var1,var2,var3,var4,var5,var6,var7,var8,var9,var10,var11,var12,var13,var14,var15,var16]
	# selfCheck = checkDuplicateSelfV1(tmpList,pollingNum)
	otherCheck = {}
	for var in tmpList[0:pollingNum]:
		if len(var)!=0:
			for tid in var:
				# 检查其他大屏的数据
				if checkDuplicateInOtherChannel(tid,screenID,pollingNum) == True:
					otherCheck[tid] = True
	# print 'selfCheck is ',selfCheck
	# 没有重复，完全正确
	# if selfCheck==False and len(otherCheck) == 0:
	if len(otherCheck) == 0:
		return False
	returnString = u""
	# if selfCheck!=False:
	# 	returnString += u"本屏内重复的视频通道为："
	# 	for item in selfCheck:
	# 		returnString+=terminalArray.objects.get(pk=int(item)).name
	# 		returnString += " "
	# 	returnString += "\r\n"
	if len(otherCheck) != 0:
		returnString += u"与其他大屏重复的视频通道为："
		for item in otherCheck:
			returnString+=terminalArray.objects.get(pk=int(item)).name
			returnString += " "
	return returnString
# 检查tid在其他大屏中是否重复项	,只检测在其他大屏的分屏数范围内。超范围的不管
# 发现重复返回 True
# 没有重复的返回False
def checkDuplicateInOtherChannel(tid,channelID,pollingNum):
	channelList = channel.objects.filter(active = True).exclude(pk = int(channelID))
	for otherChannel in channelList:
		pollingNum = otherChannel.saperateNumber
		curPollingPos = otherChannel.pollingPos
		# 1:2,3,7, 2:-1 3:3,4,5,

		posList = curPollingPos.split(" ")
		# 1:1,2,3,4,
		i = 1
		tmpList = []
		for posInSingleScreen in posList:
			if i <= pollingNum:
				tempList = []
				clip = "^"+str(i)+":.+,$"
				if len(re.findall(clip,posInSingleScreen)) != 0:
					# 去掉如 1: 2:
					newPosInSingleScreen = re.sub(str(i)+":",'',posInSingleScreen)

					newPosInSingleScreen = re.sub(",$",'',newPosInSingleScreen)
					finalPosList = newPosInSingleScreen.split(",")
					tmpList.append(finalPosList)
			i+=1
		if checkDuplicate(tid,tmpList,pollingNum):
			return True
		else:
			return False
# 检查tmpList中自身是否有重复项
# tmpList: [u'2', u'3', u'7'] [] [u'11'] [u'5'] [u'1'] [u'6'] [] [] []
# 发现重复返回重复ID 格式为{}
# 没有重复的返回False
def checkDuplicateSelfV1(tmpList,pollingNum):
	tmpDict = {}
	duplicatedID = {}
	for var in tmpList[0:pollingNum]:
		if len(var)!=0:
			for item in var:
				if str(item) not in tmpDict:
					tmpDict[str(item)] = True
					continue
				elif tmpDict[str(item)] == True and int(item)!= -1:
					duplicatedID[item] = True
	if len(duplicatedID) == 0:
		return False
	else:
		return duplicatedID

# 检查tid在tmpList中是否有重复项
# tmpList: [u'2', u'3', u'7'] [] [u'11'] [u'5'] [u'1'] [u'6'] [] [] []
# 发现重复返回 True
# 没有重复的返回False
def checkDuplicate(tid,tmpList,pollingNum):
	tmpDict = {}
	for var in tmpList[0:pollingNum]:
		if len(var)!=0:
			for item in var:
				if str(item) not in tmpDict:
					tmpDict[str(item)] = True
					continue
				# elif tmpDict[str(item)] == True and int(item)!= -1:
				# 	print u"checkDuplicate is ",item
				# 	return True
	if str(tid) not in tmpDict:
		return False
	else:
		return True

@login_required
@csrf_exempt
def configPolling(request,channelID,channelNum):
	if request.POST:
		# 校验数据是否合法，不合法则返回错误提示
		# checkResult = checkPostDate(request,channelID,channelNum)
		# if checkResult!=False:
		# 	return HttpResponse(checkResult)
		curChannel = channel.objects.get(pk=channelID)
		terminalList = terminal.objects.all()
		dstList = []
		# *******************************************************************************************************************
		# 1分屏的轮巡
		if channelNum == "1":
			return postPollingWithNum(request,1,channelID)
		# *******************************************************************************************************************
		# 1分屏的轮巡
		if channelNum == "2":
			return postPollingWithNum(request,2,channelID)
		# *******************************************************************************************************************
		# 3分屏的轮巡
		if channelNum == "3":
			return postPollingWithNum(request,3,channelID)
		# *******************************************************************************************************************
		# 4分屏的轮巡
		if channelNum == "4":
			print "configPolling 4"
			return postPollingWithNum(request,4,channelID)
		# *******************************************************************************************************************
		# 4分屏的轮巡
		if channelNum == "6":
			print "configPolling 6"
			return postPollingWithNum(request,6,channelID)
		# *******************************************************************************************************************
		# 9分屏的轮巡
		if channelNum == "9":
			print "configPolling 9"
			return postPollingWithNum(request,9,channelID)
		# *******************************************************************************************************************
		# 16分屏的轮巡
		if channelNum == "16":
			print "configPolling 16"
			return postPollingWithNum(request,16,channelID)
		# *******************************************************************************************************************
		# 20分屏的轮巡
		if channelNum == "20":
			print "configPolling 20"
			return postPollingWithNum(request,20,channelID)

	else:
		curChannel = channel.objects.get(pk=channelID)
		terminalList = terminalArray.objects.filter(status = True)
		dstList = []
		# 1分屏的轮巡
		if channelNum == "1":
			return getPollingWithNum(request,1,channelID)
		if channelNum == "2":
			return getPollingWithNum(request,2,channelID)
		if channelNum == "3":
			return getPollingWithNum(request,3,channelID)
		# 4分屏的轮巡
		if channelNum == "4":
			return getPollingWithNum(request,4,channelID)
		# 4分屏的轮巡
		if channelNum == "6":
			return getPollingWithNum(request,6,channelID)
		# 9分屏的轮巡
		if channelNum == "9":
			return getPollingWithNum(request,9,channelID)
		if channelNum == "16":
			return getPollingWithNum(request,16,channelID)
		if channelNum == "20":
			return getPollingWithNum(request,20,channelID)
		else:
			return render(request,'base/configPolling9.html',{'terminals':terminalList,'curChannel':curChannel,'channelID':channelID,'dstList':finalPosListWithName})

@csrf_exempt
def hsInterface(request):
	if request.POST:
		PORT = 12310
		HOST="localhost"

		ADDR=(HOST,PORT)

		TerminalIp = request.POST.get('TerminalIp')
		Position = request.POST.get('Position')
		print TerminalIp
		print Position
		pos = Position.split(',')
		if len(pos) == 2:
			pos = pos[1]
		else:
			pos = ""

		if pos is "":
			return HttpResponse("OK")

		pos = int(pos) + 1

		tid = -1;
		t = terminalArray.objects.filter(ip=TerminalIp)
		if len(t)!=0:
			t = t[0]
			print t
			if(t.status):
				tid = t.pk
		else:
			pass

		if tid == -1:
			return HttpResponse("OK")

		for screen in channel.objects.filter(active=True):
			if screen.active and screen.inUse and screen.saperateNumber==20:
				print screen
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
					print "0---------",rawPosition
                    # replace 0,1 position to huishang result

					i = pos
					pollingPos = ""

					if i == 1:
						clip = "^"+str(i)+":-?(\d{1,10000},){1,10000}"
						pollingPos = re.sub(clip,str(i)+":"+str(tid)+",",rawPosition)
						print str(i)+":"+str(tid),"  ",pollingPos
					else:
						clip = " "+str(i)+":-?(\d{1,10000},){1,10000}"
						pollingPos = re.sub(clip," "+str(i)+":"+str(tid)+",",rawPosition)
						print str(i)+":"+str(tid),"  ",pollingPos

					if len(pollingPos)==0:
						return HttpResponse("OK")

					print "1--------",pollingPos
					# for pos in posBytesToSave:
					# 	pollingPos += (pos+" ")
					pollingPos = pollingPos.lstrip()
					pollingPos = pollingPos.rstrip()
					screen.pollingPos = pollingPos
					screen.save()

					posList = pollingPos.split(" ")
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

					print msgToSend
					# msgToSend.cpl.terminalID.append(str(item))
					# print msgToSend
					pollingContent = msgToSend.SerializeToString()
					tcpCliSock = socket(AF_INET,SOCK_STREAM)
					tcpCliSock.connect(ADDR)
					tcpCliSock.send(pollingContent)
					tcpCliSock.close()
				except Exception as e2:
					print "send screen id %d error"%int(screen.pk),e2




		return HttpResponse("OK")
	else:
		return HttpResponse("OK")
