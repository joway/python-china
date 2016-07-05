from django.test import TestCase

from users.services import AuthService


class AuthServiceTestCase(TestCase):
    def setUp(self):
        pass

    def login(self):
        AuthService.get_tokens()
