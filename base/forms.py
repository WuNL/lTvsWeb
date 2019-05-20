# -*- coding: UTF-8 -*-
from base.models import *
from django.forms import ModelForm,ValidationError,TextInput
from django import forms

class channelForm(ModelForm):
	class Meta:
		model = channel
		fields = ['name','content',]
		widgets = {
		'name':TextInput(attrs={'class':'text-input small-input',}),
		# 'saperateNumber':TextInput(attrs={'class':'text-input small-input',}),
		# 'pos':TextInput(attrs={'class':'text-input small-input',}),
		'content':TextInput(attrs={'class':'text-input small-input',}),
		}

class terminalForm(ModelForm):
	class Meta:
		model = terminal
		fields = ['name','terminalIP',]
		widgets = {
		'name':TextInput(attrs={'class':'text-input small-input',}),
		'terminalIP':TextInput(attrs={'class':'text-input small-input',}),
		# 'pos':TextInput(attrs={'class':'text-input small-input',}),
		# 'pos':TextInput(attrs={'class':'text-input small-input',}),
		}