from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns(
    '',
    url(r'^thememaker/$', views.index),
    url(r'^thememaker/new/(?P<page_number>\d*)$', views.new),
    url(r'^thememaker/hot/(?P<page_number>\d*)$', views.hot),
    url(r'^thememaker/fav/(?P<page_number>\d*)$', views.fav),
    url(r'^thememaker/create/$', views.create),
    url(r'^thememaker/submit/$', views.submit),
    url(r'^thememaker/preview/$', views.preview),
    url(r'^thememaker/theme/(?P<theme_id>\d*)$', views.theme),
)
