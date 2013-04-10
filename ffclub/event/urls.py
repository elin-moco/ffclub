from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns(
    '',
    url(r'^events/$', views.wall, name='event.wall'),
    url(r'^events/(?P<page_number>\d+)$', views.wall_page, name='event.wall.page'),
    url(r'^events/photos/(?P<photo_id>\d+)$', views.event_photo, name='event.photo'),
)
