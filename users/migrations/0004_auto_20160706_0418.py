# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-05 20:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20160630_2307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='create_at',
            new_name='created_at',
        ),
        migrations.RemoveField(
            model_name='user',
            name='alink_verify_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_alink_verify_time',
        ),
        migrations.RemoveField(
            model_name='user',
            name='school',
        ),
    ]