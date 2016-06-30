from json import JSONDecodeError

import requests
from django.utils.http import urlencode

from config.settings import SOCIAL_AUTH_GITHUB_KEY, SOCIAL_AUTH_GITHUB_SECRET, \
    SOCIAL_AUTH_CODING_KEY, SOCIAL_AUTH_CODING_SECRET, SOCIAL_AUTH_QQ_KEY, SOCIAL_AUTH_QQ_SECRET, \
    CODING_SOCIAL_CALLBACK_REDIRECT_URL, QQ_SOCIAL_CALLBACK_REDIRECT_URL, GITHUB_SOCIAL_CALLBACK_REDIRECT_URL
from social.exceptions import SocialOauthProcessError, UserInfoError


class SocialBaseOauth(object):
    AUTH_URL = ''
    USER_URL = ''
    ACCESS_TOKEN_URL = ''
    PROVIDER = ''

    CLIENT_ID = ''
    CLIENT_SECRET = ''

    AUTH_DATA = {}

    UNIQUE_FIELD = 'id'

    HEADER = {"Accept": "application/json"}

    USERNAME_FIELD = 'username'

    @classmethod
    def get_token_data(cls, code):
        return {
            'code': code,
            'client_id': cls.CLIENT_ID,
            'client_secret': cls.CLIENT_SECRET,
            'grant_type': "authorization_code"
        }

    @classmethod
    def get_tokens(cls, code):
        try:
            tokens = requests.get(url=cls.ACCESS_TOKEN_URL, params=cls.get_token_data(code=code),
                                  headers=cls.HEADER).json()
        except JSONDecodeError:
            raise SocialOauthProcessError
        access_token = tokens.get('access_token', None)
        refresh_token = tokens.get('refresh_token', None)
        return access_token, refresh_token

    @classmethod
    def get_user_info(cls, access_token):
        _data = {'access_token': access_token}
        try:
            info = requests.get(url=cls.USER_URL,
                                params=_data,
                                headers=cls.HEADER
                                ).json()
            return info
        except JSONDecodeError:
            raise SocialOauthProcessError

    @classmethod
    def get_auth_url(cls):
        return cls.AUTH_URL + '?' + urlencode(cls.AUTH_DATA)

    @classmethod
    def callback_url(cls):
        return SOCIAL_CALLBACK_REDIRECT_BASE_URL + cls.PROVIDER

    @classmethod
    def get_provider(cls):
        return cls.PROVIDER

    @classmethod
    def get_unique_id(cls, access_token=None, info=None):
        if not info and access_token:
            info = cls.get_user_info(access_token=access_token)
        try:
            return info[cls.UNIQUE_FIELD]
        except:
            raise UserInfoError

    @classmethod
    def get_username(cls, access_token=None, info=None):
        if info and access_token is not None:
            info = cls.get_user_info(access_token=access_token)
        try:
            return info[cls.USERNAME_FIELD]
        except KeyError:
            raise UserInfoError


class GithubSocialOauth(SocialBaseOauth):
    PROVIDER = 'github'
    AUTH_URL = 'https://github.com/login/oauth/authorize'
    USER_URL = 'https://api.github.com/user'
    ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'

    CLIENT_ID = SOCIAL_AUTH_GITHUB_KEY
    CLIENT_SECRET = SOCIAL_AUTH_GITHUB_SECRET

    UNIQUE_FIELD = 'email'
    USERNAME_FIELD = 'username'

    AUTH_DATA = {
        'client_id': SOCIAL_AUTH_GITHUB_KEY,
        'redirect_uri': GITHUB_SOCIAL_CALLBACK_REDIRECT_URL,
        'scope': 'user',
        'state': 'joway',
    }


class CodingSocialOauth(SocialBaseOauth):
    PROVIDER = 'coding'
    AUTH_URL = 'https://coding.net/oauth_authorize.html'
    USER_URL = 'https://coding.net/api/current_user'
    ACCESS_TOKEN_URL = 'https://coding.net/api/oauth/access_token'

    CLIENT_ID = SOCIAL_AUTH_CODING_KEY
    CLIENT_SECRET = SOCIAL_AUTH_CODING_SECRET

    AUTH_DATA = {
        'client_id': CLIENT_ID,
        'redirect_uri': CODING_SOCIAL_CALLBACK_REDIRECT_URL,
        'response_type': 'code',
        'scope': 'user',
    }

    UNIQUE_FIELD = 'id'
    USERNAME_FIELD = 'name'

    @classmethod
    def get_user_info(cls, access_token):
        return super(CodingSocialOauth, cls).get_user_info(access_token=access_token)['data']


class QQSocialOauth(SocialBaseOauth):
    PROVIDER = 'qq'

    AUTH_URL = 'https://graph.qq.com/oauth2.0/authorize'
    USER_URL = 'https://graph.qq.com/oauth2.0/me'
    ACCESS_TOKEN_URL = 'https://graph.qq.com/oauth2.0/token'

    CLIENT_ID = SOCIAL_AUTH_QQ_KEY
    CLIENT_SECRET = SOCIAL_AUTH_QQ_SECRET

    UNIQUE_FIELD = 'id'

    AUTH_DATA = {
        'client_id': CLIENT_ID,
        'redirect_uri': QQ_SOCIAL_CALLBACK_REDIRECT_URL,
        'response_type': 'code',
        'state': 'joway'
    }

    @classmethod
    def get_token_data(cls, code):
        return {
            'code': code,
            'client_id': cls.CLIENT_ID,
            'client_secret': cls.CLIENT_SECRET,
            'grant_type': "authorization_code",
            'redirect_uri': SOCIAL_CALLBACK_REDIRECT_BASE_URL + PROVIDER
        }
