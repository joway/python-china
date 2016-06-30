from django.utils import timezone
from oauthlib.common import UNICODE_ASCII_CHARACTER_SET
from oauthlib.common import generate_client_id as oauthlib_generate_client_id
from oauthlib.common import generate_token as oauthlib_generate_token


def generate_client_id():
    """
        Generate a suitable client id
        """
    return oauthlib_generate_client_id(length=128,
                                       chars=UNICODE_ASCII_CHARACTER_SET)


def generate_client_secret():
    """
        Generate a suitable client secret
     """
    return oauthlib_generate_client_id(length=40, chars=UNICODE_ASCII_CHARACTER_SET)


def generate_access_token():
    return oauthlib_generate_token(length=40)


def generate_refresh_token():
    return oauthlib_generate_token(length=40)


def generate_grant_code():
    return oauthlib_generate_token(length=40)


def token_expire_at_time():
    return (timezone.now() + timezone.timedelta(days=30))


def grant_expire_at_time():
    return (timezone.now() + timezone.timedelta(minutes=10))


def refresh_tokens(refresh_token):
    return generate_access_token(), generate_refresh_token()
