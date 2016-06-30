# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-28 02:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0004_grant_expire_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grant',
            name='code',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='授权码'),
        ),
    ]