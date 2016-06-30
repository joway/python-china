# Create your tests here.
from rest_framework.test import force_authenticate

from oauth.apis import OauthViewSet
from oauth.generators import generate_client_id, generate_client_secret
from oauth.models import Application, Grant, Token
from utils.tests import BaseTestCase


class OauthTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.base_url = '/oauth/'

        self.app_name = 'app'
        self.app_desc = '描述内容'
        self.site_url = 'http://joway.wang/callback'
        self.redirect_uri = 'http://joway.wang'

        self.client = Application.objects.create(name=self.app_name, description=self.app_desc,
                                                 redirect_uri=self.redirect_uri,
                                                 owner=self.user)

        self.grant = Grant.objects.create_grant(app=self.client, user=self.user)

    def test_oauth_service(self):
        client_id = generate_client_id()
        client_secret = generate_client_secret()
        print(client_id)
        print(client_secret)

    def test_register(self):
        data = {
            'name': self.app_name,
            'description': self.app_desc,
            'redirect_uri': self.redirect_uri,
            'site_uri': self.site_url,
        }

        viewset = OauthViewSet.as_view(actions={'post': 'register'})
        request = self.factory.post(self.base_url + 'register/', data=data)
        force_authenticate(request, user=self.user)
        response = viewset(request)
        print(response.data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['name'], self.app_name)
        self.assertEquals(response.data['description'], self.app_desc)
        self.assertEquals(response.data['site_uri'], self.site_url)
        self.assertEquals(response.data['redirect_uri'], self.redirect_uri)

        viewset = OauthViewSet.as_view(actions={'get': 'applications'})
        request = self.factory.get(self.base_url + 'applications/')
        force_authenticate(request, user=self.user)
        response = viewset(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data[0]['name'], self.app_name)

    def test_auth(self):
        viewset = OauthViewSet.as_view(actions={'post': 'authorize'})

        data = {
            'client_id': self.client.client_id,
            'redirect_url': self.client.redirect_uri
        }
        response = viewset(self.auth_post(self.base_url + 'authorize/', data=data))
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_access_token(self):
        viewset = OauthViewSet.as_view(actions={'post': 'access_token'})
        print(self.grant)
        data = {
            'client_id': self.client.client_id,
            'client_secret': self.client.client_secret,
            'redirect_url': self.client.redirect_uri,
            'code': self.grant.code,
        }
        response = viewset(self.auth_post(self.base_url + 'access_token/', data=data))
        print(response.data)
        self.assertEqual(response.status_code, 200)

    def test_refresh_token(self):
        viewset = OauthViewSet.as_view(actions={'post': 'refresh_token'})
        self.token = Token.objects.create_token(self.client, user=self.user)
        data = {
            'client_secret': self.client.client_secret,
            'client_id': self.client.client_id,
            'refresh_token': self.token.refresh_token,
        }
        response = viewset(self.auth_post(self.base_url + 'refresh_token/', data=data))
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertNotEquals(response.data['access_token'], self.token.access_token)

    def get_user(self):
        viewset = OauthViewSet.as_view(actions={'post': 'user'})
        self.token = Token.objects.create_token(self.client, user=self.user)
        data = {
            'access_token': self.token.access_token,
        }
        response = viewset(self.auth_post(self.base_url + 'user/', data=data))
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.user.username)
