# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
#终端
class terminal(models.Model):
	terminalIP = models.GenericIPAddressField(unique=True,max_length=200,blank=False,null=False,verbose_name=u"IP",error_messages={'unique':u"重复IP,请重新输入!"})
	name = models.CharField(max_length=200,blank=False,null=False,verbose_name=u"终端名称")

#大屏
class channel(models.Model):
	name = models.CharField(max_length=200,blank=False,null=False,verbose_name=u"名称")
	# channelID = models.IntegerField(blank=False,null=False,verbose_name=u"ID")
	saperateNumber = models.IntegerField(blank=False,null=False,verbose_name=u"分屏数")
	content = models.CharField(max_length=200,blank=False,null=False,verbose_name=u"内容")
	# 1-1 2-3 2-4
	pos = models.CharField(max_length=200,blank=True,null=True,verbose_name=u"位置")
	polling = models.BooleanField(default=False,verbose_name=u"轮巡状态")
	# 
	pollingPos = models.CharField(max_length=2000,blank=True,null=True,verbose_name=u"轮巡位置")
	pollingTime = models.IntegerField(default=15,blank=False,null=False,verbose_name=u"轮巡间隔时间(秒)")

	#
	active = models.BooleanField(default=False,verbose_name=u"显示器是否激活")
	inUse = models.BooleanField(default=True,verbose_name=u"window是否used")
	monitorName = models.CharField(max_length=200,blank=True,null=True,verbose_name=u"显示器名称")
	GPUSeq = models.CharField(max_length=200,blank=True,null=True,verbose_name=u"GPUSeq")
	freshRate = models.CharField(max_length=200,blank=True,null=True,verbose_name=u"显示器FreshRate")
	resolution = models.CharField(max_length=200,blank=True,null=True,verbose_name=u"显示器分辨率")
	productID = models.CharField(max_length=200,blank=True,null=True,verbose_name=u"显示器产品ID")


#20路数组
class terminalArray(models.Model):
	ip = models.GenericIPAddressField(unique=True,max_length=200,blank=True,null=True,verbose_name=u"IP")
	name = models.CharField(max_length=190,blank=True,null=True,verbose_name=u"名称")
	status = models.BooleanField(default=False,verbose_name=u"当前状态")