from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate

from config.settings import JWT_AUTH
from social.apis import SocialAuthViewSet
from .models import User


class SocialOauthTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.base_url = '/social/'
        self.username = 'joway'
        self.email = '670425438@qq.com'
        self.password = 'password'
        self.provider = 'coding'
        # 有时效限制,过一段时间跑会出现解析错误
        self.code = '6934b5d588d30dab3bd34919a3e0e88a'
        self.user = User.objects.create_activate_user(username=self.username, email=self.email,
                                                      password=self.password)

        self.settings(EMAIL_BACKEND='sendcloud.SendCloudBackend',
                      MAIL_APP_USER='jowaywong',
                      MAIL_APP_KEY='fwPcJDvCdgEHsuLt',
                      DEFAULT_FROM_EMAIL='admin@joway.wang',
                      JWT_AUTH=JWT_AUTH)

    def login(self):
        viewset = SocialAuthViewSet.as_view(actions={'post': 'login'})
        data = {
            'code': self.code,
            'provider': self.provider
        }

        # 准备数据
        viewset_binding = SocialAuthViewSet.as_view(actions={'post': 'binding'})
        request = self.factory.post(self.base_url + 'binding/', data=data)
        force_authenticate(request, user=self.user)
        viewset_binding(request)

        request = self.factory.post(self.base_url + 'login/', data=data)
        response = viewset(request)
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def binding(self):
        viewset = SocialAuthViewSet.as_view(actions={'post': 'binding'})
        data = {
            'code': self.code,
            'provider': self.provider
        }
        request = self.factory.post(self.base_url + 'binding/', data=data)
        force_authenticate(request, user=self.user)
        response = viewset(request)
        print(response.data)
        self.assertEqual(response.status_code, 200)
