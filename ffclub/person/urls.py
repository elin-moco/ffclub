from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns('',
                       url(r'^users/register/$', views.register, name='user.register'),
                       url(r'^users/register/complete/$', views.register_complete, name='user.register.complete'),
)
