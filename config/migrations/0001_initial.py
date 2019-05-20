# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-07 05:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='debugStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debugStatus', models.BooleanField(default=False, verbose_name='\u662f\u5426\u8bb0\u5f55\u8c03\u8bd5\u65e5\u5fd7')),
            ],
        ),
        migrations.CreateModel(
            name='packetGrepper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(default='192.168.1.1', unique=True, verbose_name='IP')),
                ('active', models.BooleanField(default=False, verbose_name='\u662f\u5426\u542f\u7528\u6293\u5305\u670d\u52a1\u5668')),
            ],
        ),
        migrations.CreateModel(
            name='packetsLostInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terminalName', models.CharField(max_length=300)),
                ('latestLostDate', models.CharField(max_length=300)),
                ('lostNumbers', models.IntegerField(default=0)),
                ('totalPacketNumbers', models.IntegerField(default=0)),
                ('status', models.BooleanField(default=False, verbose_name='\u662f\u5426\u6709\u6548')),
            ],
        ),
        migrations.CreateModel(
            name='registerStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resgisterStatus', models.BooleanField(default=False, verbose_name='\u7cfb\u7edf\u6ce8\u518c\u72b6\u6001')),
            ],
        ),
        migrations.CreateModel(
            name='userLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=3000)),
                ('date', models.DateTimeField(auto_now=True)),
                ('target', models.CharField(max_length=3000)),
                ('content', models.CharField(max_length=3000)),
            ],
        ),
    ]
