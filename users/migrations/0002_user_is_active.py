# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-27 01:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='邮箱激活'),
        ),
    ]
