from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns('',
    url(r'^events/$', views.wall, name='event.wall'),
)
