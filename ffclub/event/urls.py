from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns(
    '',
    url(r'^events/$', views.wall, name='event.wall'),
    url(r'^events/(?P<page_number>\d+)$', views.wall_page, name='event.wall.page'),
    url(r'^events/photos/(?P<photo_id>\d+)$', views.event_photo, name='event.photo'),
    url(r'^events/photos/(?P<photo_id>\d+)/report$', views.event_photo_report, name='event.photo.report'),
    url(r'^events/photos/(?P<photo_id>\d+)/remove$', views.event_photo_remove, name='event.photo.remove'),
)
