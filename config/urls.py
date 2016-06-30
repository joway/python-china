from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from config import views
from .router import router

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^topic$', views.topic, name='index'),
    url(r'^admin/', include(admin.site.urls)),

    url(r"^", include(router.urls)),

    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-captcha/', verify_jwt_token),
]
