from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='intro.home'),
    url(r'^index/$', views.index, name='intro.index'),
    url(r'^browserid/', include('django_browserid.urls')),
    url(r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/'},
        name='intro.logout'),
)
