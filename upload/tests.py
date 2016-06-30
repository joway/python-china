from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate

from config.settings import JWT_AUTH
from .apis import UploadViewSet
from users.models import User


class SocialOauthTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.base_url = '/upload/'
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

    def test_token(self):
        viewset = UploadViewSet.as_view(actions={'post': 'token'})

        request = self.factory.post(self.base_url + 'token/')
        force_authenticate(request, user=self.user)
        response = viewset(request)
        print(response.data)
        self.assertEqual(response.status_code, 200)
