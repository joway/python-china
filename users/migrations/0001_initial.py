# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-26 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                                                     help_text='Designates that this user has all permissions without explicitly assigning them.',
                                                     verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='注册邮箱')),
                ('username', models.CharField(db_index=True, default='', max_length=255, verbose_name='昵称')),
                ('school', models.CharField(max_length=255, null=True, verbose_name='目前的学校')),
                ('sex', models.BooleanField(choices=[(False, '男'), (True, '女')], default=False, verbose_name='性别')),
                ('birthday', models.DateField(null=True, verbose_name='生日')),
                ('score', models.IntegerField(default=0, verbose_name='积分')),
                ('is_staff', models.BooleanField(default=False, verbose_name='管理员')),
                ('avatar', models.URLField(blank=True, max_length=255, null=True, verbose_name='头像')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='帐号创建时间')),
                ('alink_verify_code', models.CharField(blank=True, max_length=32, null=True, verbose_name='激活链接验证码')),
                ('last_alink_verify_time',
                 models.DateTimeField(blank=True, null=True, verbose_name='上一次激活链接发送请求验证码请求时间')),
                ('groups', models.ManyToManyField(blank=True,
                                                  help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                                                  related_name='user_set', related_query_name='user', to='auth.Group',
                                                  verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.',
                                                            related_name='user_set', related_query_name='user',
                                                            to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
