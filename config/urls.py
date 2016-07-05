from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import refresh_jwt_token

from . import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.home, name='index'),
    url(r'^topic$', views.topic, name='topic'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('users.urls')),
    url(r'^api-token-refresh/', refresh_jwt_token),

]
