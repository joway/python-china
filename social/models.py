from django.db import models

from users.models import User
from .constants import PROVIDERS_CHOICES


class SocialAccount(models.Model):
    uid = models.CharField('uid', max_length=255, null=True, blank=True)
    username = models.CharField('用户名', max_length=32, blank=True)

    expire_at = models.DateTimeField('token失效时间', blank=True, null=True)

    access_token = models.CharField('access_token', max_length=255, blank=True, null=True)
    refresh_token = models.CharField('refresh_token', max_length=255, blank=True, null=True)

    provider = models.CharField('类别', choices=PROVIDERS_CHOICES, max_length=10)
    user = models.ForeignKey(User, null=True, blank=True)
