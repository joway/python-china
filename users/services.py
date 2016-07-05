import requests
from django.utils.http import urlencode

from config.settings import AUTH_BASE_URL
from users.exceptions import AuthProcessError


class AuthService(object):
    AUTH_URL = AUTH_BASE_URL + '/oauth/authorize/'
    USER_URL = AUTH_BASE_URL + '/oauth/user/'
    ACCESS_TOKEN_URL = AUTH_BASE_URL + '/oauth/access_token/'

    PROVIDER = 'AUTH'

    CLIENT_ID = 'LlLvZNh9FMbc62K4OA1yjq9CWFoEx12OWBwSYKVlK1qOhUegA6VjAqVfVT8HrbxCdvr4FPfiThI013UnXA7LaBY5WnpsnNo0UNh906Kzj85bI7ukH1Ay0u96SgsyRD2C'
    CLIENT_SECRET = 'kApfnMdip0QkqdKdhE3YJZAq0raxmpJ7nCZd1sYB'

    AUTH_DATA = {
        'client_id': CLIENT_ID,
    }

    UNIQUE_FIELD = 'email'

    HEADER = {"Accept": "application/json"}

    USERNAME_FIELD = 'username'

    @classmethod
    def get_token_data(cls, code):
        return {
            'code': code,
            'client_id': cls.CLIENT_ID,
            'client_secret': cls.CLIENT_SECRET,
            'grant_type': "jwt_bearer"
        }

    @classmethod
    def get_tokens(cls, code):
        try:
            tokens = requests.post(url=cls.ACCESS_TOKEN_URL, data=cls.get_token_data(code=code),
                                   headers=cls.HEADER).json()
        except:
            raise AuthProcessError
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
        except:
            raise AuthProcessError

    @classmethod
    def get_auth_url(cls):
        return cls.AUTH_URL + '?' + urlencode(cls.AUTH_DATA)
