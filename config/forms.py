# -*- coding: UTF-8 -*-
from base.models import *
from config.models import *
from django.forms import ModelForm,ValidationError,TextInput
from django import forms

class textStyleForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super(textStyleForm,self).__init__(*args,**kwargs)
        SIZECHOICES = [('0','small'),
        ('1','medium'),
        ('2','large')
        ]
        LOCATIONCHOICES = [('0','left top'),
        ('1','left bottom'),
        ]
        COLORCHOICES = [('0','color 1'),
        ('1','color 2'),
        ('2','color 3'),
        ('3','color 4'),
        ('4','color 5'),
        ]
        self.fields['textSize'] = forms.ChoiceField(label="textSize123",initial=('1','medium'),choices=SIZECHOICES,required=True)
        self.fields['location'] = forms.ChoiceField(label="location",choices=LOCATIONCHOICES,initial=('5','right bottom'),required=True)
        self.fields['color'] = forms.ChoiceField(label="color",choices=COLORCHOICES,initial=('0','color 1'),required=True)
        self.fields['showFps'] = forms.BooleanField(label="show FPS",required=False)
    class Meta:
        model = textStyle
        fields = '__all__'
        # widgets = {
        # 'textSize':TextInput(attrs={'class':'text-input small-input',}),
        # 'location':TextInput(attrs={'class':'text-input small-input',}),
        # }
