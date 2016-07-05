from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns(
    'users',
    url(r'^redirect/$', views.redirect),
    url(r'^callback/$', views.callback),
    url(r'^login/$', views.login),
)
