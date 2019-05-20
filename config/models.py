# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class registerStatus(models.Model):
	resgisterStatus = models.BooleanField(default=False,verbose_name=u"系统注册状态")

class debugStatus(models.Model):
	debugStatus = models.BooleanField(default=False,verbose_name=u"是否记录调试日志")

class userLog(models.Model):
	user = models.CharField(max_length=3000)
	date = models.DateTimeField(auto_now=True)
	target = models.CharField(max_length=3000)
	content = models.CharField(max_length=3000)

class packetsLostInfo(models.Model):
	terminalName = models.CharField(max_length=300)
	latestLostDate = models.CharField(max_length=300)
	lostNumbers = models.IntegerField(default = 0)
	totalPacketNumbers = models.IntegerField(default = 0)
	status = models.BooleanField(default=False,verbose_name=u"是否有效")

class packetGrepper(models.Model):
	ip = models.GenericIPAddressField(unique=True,max_length=200,blank=False,null=False,verbose_name=u"IP",default="192.168.1.1")
	active = models.BooleanField(default=False,verbose_name=u"是否启用抓包服务器")
class textStyle(models.Model):
	textSize = models.IntegerField(default = 1)
	location = models.IntegerField(default = 0)
	color = models.IntegerField(default = 0)
	showFps = models.BooleanField(default=True,verbose_name=u"是否Show FPS")
