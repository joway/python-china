from rest_framework import routers

from oauth.apis import OauthViewSet
from social.apis import SocialAuthViewSet
from users.apis import ProfileViewSet, AuthViewSet

router = routers.DefaultRouter(trailing_slash=True)

router.register(r"user", ProfileViewSet, base_name="user")
router.register(r"auth", AuthViewSet, base_name="auth")
router.register(r"social", SocialAuthViewSet, base_name="social")
router.register(r"oauth", OauthViewSet, base_name="oauth")
