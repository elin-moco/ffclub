from django.conf.urls import *

from . import views


urlpatterns = patterns(
    '',
    url(r'^events/$', views.wall, name='event.wall'),
    url(r'^events/(?P<page_number>\d+)$', views.wall_page, name='event.wall.page'),
    url(r'^(?P<type>event|campaign)/photos/(?P<photo_id>\d+)/$', views.activity_photo, name='activity.photo'),
    url(r'^(?P<type>event|campaign)/photos/(?P<photo_id>\d+)/report/$', views.activity_photo_report, name='activity.photo.report'),
    url(r'^(?P<type>event|campaign)/photos/(?P<photo_id>\d+)/remove/$', views.activity_photo_remove, name='activity.photo.remove'),
    url(r'^campaign/every-moment/$', views.every_moment, name='campaign.every.moment'),
    url(r'^campaign/every-moment/upload/$', views.every_moment_upload, name='campaign.every.moment.upload'),
    url(r'^campaign/every-moment/wall/$', views.every_moment_wall, name='campaign.every.moment.wall'),
    url(r'^campaign/every-moment/wall/(?P<page_number>\d+)$', views.wall_page, name='campaign.every.moment.wall.page'),
    url(r'^events/attack-on-web/$', views.attack_on_web, name='event.attack.on.web'),
    url(r'^events/attack-on-web/prizes/$', views.prizes, name='event.attack.on.web.prizes'),
    url(r'^events/attack-on-web/apply/$', views.apply, name='event.attack.on.web.apply'),
    url(r'^events/attack-on-web/demo$/', views.demo, name='event.attack.on.web.demo'),
    url(r'^events/attack-on-web/microfilm/$', views.microfilm, name='event.attack.on.web.microfilm'),
)
