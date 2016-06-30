from django.utils import timezone

from config.settings import DOMAIN_URL
from sendcloud.constants import SendCloudTemplates
from sendcloud.exceptions import SendcloudError
from sendcloud.utils import sendcloud_template
from utils.jwt import get_jwt_token
from utils.utils import get_random_string
from .constants import MAX_MAIL_INTERVAL_SECONDS, ALINK_VERIFY_CODE_LENGTH, MAX_MAIL_VALID_SECONDS
from .exceptions import UserNotExist, PasswordError, EmailExist, VerifyTimeFrequently, VerifyCodeError, \
    UserHasActivated, VerifyCodeExpire
from .models import User


class UserService(object):
    @classmethod
    def login(cls, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise UserNotExist
        if user.check_password(password):
            return get_jwt_token(user)
        else:
            raise PasswordError

    @classmethod
    def register(cls, email, password):
        user, is_create = User.objects.get_or_create(email=email)
        if not is_create:
            raise EmailExist

        if user.last_alink_verify_time and (
                    timezone.now() - user.last_alink_verify_time).seconds < MAX_MAIL_INTERVAL_SECONDS:
            raise VerifyTimeFrequently

        user.set_password(password)
        user.alink_verify_code = get_random_string(ALINK_VERIFY_CODE_LENGTH)
        user.last_alink_verify_time = timezone.now()
        if sendcloud_template(to=[email],
                              tpt_ivk_name=SendCloudTemplates.REGISTER,
                              sub_vars={'%username%': [email],
                                        '%url%': [DOMAIN_URL + '/user/activate?confirm=' + user.alink_verify_code]}):
            user.save()
            return user
        else:
            raise SendcloudError

    @classmethod
    def activate(cls, alink_verify_code):
        try:
            user = User.objects.get(alink_verify_code=alink_verify_code)
        except User.DoesNotExist:
            raise VerifyCodeError
        if not user.is_active:
            raise UserHasActivated
        if (timezone.now() - user.last_alink_verify_time).seconds < MAX_MAIL_VALID_SECONDS:
            user.alink_verify_code = None
            user.is_active = True
            user.save()
            return user
        else:
            raise VerifyCodeExpire

    @classmethod
    def disactivate(cls, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise UserNotExist
        if not user.is_active:
            return False
        user.is_active = False
        user.save()
        return True

    @classmethod
    def logout(cls):
        pass
