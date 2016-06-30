from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, force_authenticate

from config.settings import JWT_AUTH
from users.apis import AuthViewSet, ProfileViewSet
from users.models import User
from users.services import UserService


class ProfileTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.base_url = '/user/'
        self.username = 'joway'
        self.email = '670425438@qq.com'
        self.password = 'password'

        self.user = User.objects.create_activate_user(username=self.username, email=self.email,
                                                      password=self.password)

        self.settings(EMAIL_BACKEND='sendcloud.SendCloudBackend',
                      MAIL_APP_USER='jowaywong',
                      MAIL_APP_KEY='fwPcJDvCdgEHsuLt',
                      DEFAULT_FROM_EMAIL='admin@joway.wang',
                      JWT_AUTH=JWT_AUTH)

    def test_profile(self):
        viewset = ProfileViewSet.as_view(actions={'get': 'list'})
        request = self.factory.get(self.base_url)
        force_authenticate(request, user=self.user)
        response = viewset(request)
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_update_profile(self):
        data = {
            'username': 'test',
        }
        viewset = ProfileViewSet.as_view(actions={'put': 'update'})
        request = self.factory.put(self.base_url, data=data)
        force_authenticate(request, user=self.user)
        response = viewset(request)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], 'test')


class AuthTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.base_url = '/auth/'
        self.username = 'joway'
        self.email = '670425438@qq.com'
        self.password = 'password'

        self.settings(EMAIL_BACKEND='sendcloud.SendCloudBackend',
                      MAIL_APP_USER='jowaywong',
                      MAIL_APP_KEY='fwPcJDvCdgEHsuLt',
                      DEFAULT_FROM_EMAIL='admin@joway.wang',
                      JWT_AUTH=JWT_AUTH)

    def test_register(self):
        viewset = AuthViewSet.as_view(actions={'post': 'register'})
        data = {
            'email': self.email,
            'password': self.password
        }
        request = self.factory.post(self.base_url + 'register/', data=data)
        response = viewset(request)
        print(response.data)
        self.assertEqual(response.status_code, 200)

        request = self.factory.post(self.base_url + 'register/', data=data)
        response = viewset(request)
        print(response.data)

        # 邮箱已被注册
        self.assertEqual(response.status_code, 403)

    def test_activate(self):
        viewset = AuthViewSet.as_view(actions={'get': 'activate'})
        self.user = UserService.register(email=self.email, password=self.password)

        data = {
            'captcha': self.user.alink_verify_code
        }
        request = self.factory.get(self.base_url + 'activate/', data=data)
        response = viewset(request)
        print(response.data)

        data = {
            'captcha': '123'
        }
        request = self.factory.get(self.base_url + 'activate/', data=data)
        response = viewset(request)
        print(response.data)
        # 验证码错误
        self.assertEqual(response.status_code, 403)

    def test_login(self):
        viewset = AuthViewSet.as_view(actions={'post': 'login'})
        self.user = UserService.register(email=self.email, password=self.password)

        data = {
            'email': self.email,
            'password': self.password
        }
        request = self.factory.post(self.base_url + 'login/', data=data)
        response = viewset(request)
        print(response.data)
        self.assertEqual(response.status_code, 200)
