from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.db import models

from .constants import ALINK_VERIFY_CODE_LENGTH


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_superuser=False, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username=username, email=email, password=password, **extra_fields)

    def create_activate_user(self, username, email, password, **extra_fields):
        return self._create_user(username=username, email=email,
                                 password=password, is_active=True, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username=username, email=email, password=password
                                 , is_superuser=True, is_staff=True, is_active=True ** extra_fields)

    def create_staff(self, username, email, password, **extra_fields):
        return self._create_user(username=username, email=email, password=password
                                 , is_superuser=False, is_staff=True, is_active=True ** extra_fields)


# Create your models here.
# 创建了自定义的User,也必须要创建自定义的UserManager
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('注册邮箱', unique=True, db_index=True)
    username = models.CharField('昵称', max_length=255, null=True, blank=True)

    school = models.CharField('目前的学校', max_length=255, null=True, blank=True)
    sex = models.BooleanField('性别', choices=((False, '男'), (True, '女')), default=False)
    birthday = models.DateField('生日', null=True, blank=True)

    score = models.IntegerField('积分', default=0)

    is_staff = models.BooleanField('管理员', default=False)

    is_active = models.BooleanField('邮箱激活', default=False)

    avatar = models.URLField('头像', max_length=255, null=True, blank=True)

    create_at = models.DateTimeField('帐号创建时间', auto_now_add=True)

    alink_verify_code = models.CharField('激活链接验证码', max_length=ALINK_VERIFY_CODE_LENGTH, blank=True, null=True)

    last_alink_verify_time = models.DateTimeField('上一次激活链接发送请求验证码请求时间', blank=True, null=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    # '-' 表示倒序
    class Meta:
        ordering = ['-id']

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return "%s (%s)" % (self.username, self.email)

    def __str__(self):
        return "%s(%s)" % (self.username, self.email)
