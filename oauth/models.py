from django.db import models

from oauth.constants import SCOPE_CHOICES, GRANT_TYPE_CHOICES, GrantTypes, Scopes
from oauth.generators import generate_client_id, generate_client_secret, generate_access_token, \
    generate_refresh_token, token_expire_at_time, grant_expire_at_time, generate_grant_code
from users.models import User


class Application(models.Model):
    owner = models.ForeignKey(User, verbose_name='应用管理员')

    name = models.CharField('应用名', max_length=255)
    description = models.CharField('描述', max_length=255, null=True, blank=True)

    client_id = models.CharField('客户端ID', max_length=255,
                                 default=generate_client_id, unique=True)
    client_secret = models.CharField('客户端密钥', max_length=255,
                                     default=generate_client_secret)

    site_uri = models.URLField('主站地址', max_length=255, null=True, blank=True)
    redirect_uri = models.URLField('回调地址', max_length=255)

    grant_type = models.CharField('授权类型', max_length=32, choices=GRANT_TYPE_CHOICES,
                                  default=(GrantTypes.AUTHORIZATION_CODE, '授权码'))


class TokensManager(models.Manager):
    def create_token(self, app, user, scope=None):
        token = self.model(application=app, user=user)
        if scope:
            token.scope = scope
        token.save(using=self._db)
        return token


class Token(models.Model):
    application = models.ForeignKey(Application, verbose_name='应用')
    user = models.ForeignKey(User, verbose_name='token持有者')

    expire_at = models.DateTimeField(verbose_name='token失效时间',
                                     default=token_expire_at_time)

    access_token = models.CharField('access_token', max_length=255, unique=True,
                                    default=generate_access_token)
    refresh_token = models.CharField('refresh_token', max_length=255, unique=True,
                                     default=generate_refresh_token)

    scope = models.TextField(max_length=32, choices=SCOPE_CHOICES, default=Scopes.Read)

    objects = TokensManager()


class GrantManager(models.Manager):
    def create_grant(self, app, user):
        grant = self.model(application=app, user=user)
        grant.save(using=self._db)
        return grant


class Grant(models.Model):
    user = models.ForeignKey(User, verbose_name='授权用户')
    application = models.ForeignKey(Application)

    expire_at = models.DateTimeField(verbose_name='token失效时间',
                                     default=grant_expire_at_time)

    code = models.CharField('授权码', max_length=255, unique=True, db_index=True,
                            default=generate_grant_code)

    scope = models.TextField('权限', max_length=32, choices=SCOPE_CHOICES, default=Scopes.Read)

    objects = GrantManager()
