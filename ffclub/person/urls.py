from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns(
    '',
    url(r'^users/register/$', views.register, name='user.register'),
    url(r'^users/register/complete/$', views.register_complete, name='user.register.complete'),
    url(r'^api/users/registered/count$', views.registered_user_count),
    url(r'^api/users/registered/(?P<provider>[-_A-z0-9]+)/count$', views.registered_user_count),

)
