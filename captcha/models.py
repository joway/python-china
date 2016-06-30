# from django.db import models
#
#
# # Create your models here.
# class BaseCaptcha(models.Model):
#     create_at = models.DateTimeField('创建时间', auto_now_add=True)
#
#     class Meta:
#         abstract = True
#
#
# class LinkCaptcha(models.Model):
#     expired_at = models.DateTimeField('过期时间')
#     captcha = models.CharField('激活链接验证码', max_length=ALINK_VERIFY_CODE_LENGTH, blank=True, null=True)
#
#
# class AuthCaptcha(models.Model):
#     expired_at = models.DateTimeField('过期时间')
#     captcha = models.CharField('激活链接验证码', max_length=ALINK_VERIFY_CODE_LENGTH, blank=True, null=True)
