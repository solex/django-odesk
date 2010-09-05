from django.conf.urls.defaults import *

urlpatterns = patterns('django_odesk.auth.views',
    url(r'^authenticate/$', 'authenticate'),
    url(r'^callback/$', 'callback'),
)
