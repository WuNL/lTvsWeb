# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-15 02:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='textStyle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('textSize', models.IntegerField(default=1)),
                ('location', models.IntegerField(default=0)),
                ('color', models.IntegerField(default=0)),
                ('showFps', models.BooleanField(default=True, verbose_name='\u662f\u5426Show FPS')),
            ],
        ),
    ]