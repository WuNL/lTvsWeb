# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-08 01:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='GPUSeq',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='GPUSeq'),
        ),
        migrations.AddField(
            model_name='channel',
            name='freshRate',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u663e\u793a\u5668FreshRate'),
        ),
    ]
