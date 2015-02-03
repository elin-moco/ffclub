# -*- coding: utf-8 -*-
from django.conf.urls import *
from . import views


urlpatterns = patterns(
    '',
    url(r'^events/$', views.wall, name='event.wall'),
    url(r'^events/(?P<page_number>\d+)/$', views.wall_page, name='event.wall.page'),
    url(r'^events/(?P<event_slug>[-_A-z0-9]+)/register/$', views.event_register, name='event.register'),
    url(r'^campaign/(?P<campaign_slug>[-_A-z0-9]+)/claim-award/$', views.campaign_claim_award,
        name='campaign.claim.award'),
    url(r'^campaign/(?P<slug>[-A-z0-9]+)/photos/(?P<photo_id>\d+)/$', views.campaign_photo, name='campaign.photo'),
    url(r'^(?P<type>event|campaign)/photos/(?P<photo_id>\d+)/$', views.activity_photo, name='activity.photo'),
    url(r'^(?P<type>event|campaign)/photos/(?P<photo_id>\d+)/report/$', views.activity_photo_report,
        name='activity.photo.report'),
    url(r'^(?P<type>event|campaign)/photos/(?P<photo_id>\d+)/remove/$', views.activity_photo_remove,
        name='activity.photo.remove'),
    url(r'^(?P<type>event|campaign)/photos/(?P<photo_id>\d+)/vote/$', views.activity_photo_vote,
        name='activity.photo.vote'),
    url(r'^(?P<type>video|demoapp)/(?P<id>[1-4])/vote/$', views.generic_vote, name='generic.vote'),

    url(r'^campaign/2014review/login/$', views.review2014_login,
        {'template': 'event/2014review-login.html'}, name='campaign.2014review.login'),
    url(r'^campaign/2014review/award/$', views.review2014_award),
    url(r'^campaign/2014review/quota/$', views.review2014_quota),
    url(r'^campaign/2014review/claim/$', views.campaign_claim_award,
        {'campaign_slug': '2014review', 'award_name': u'贈獎'}, name='campaign.2014review.claim'),

    url(r'^campaign/lantern-festival/(?P<subpath>(firefox-lantern/)?)$',
        views.lantern_festival, name='campaign.lantern.festival'),
    url(r'^campaign/lantern-festival/claim/$', views.lantern_claim_code, name='campaign.lantern.claim'),
    url(r'^campaign/chinese-valentines-day/$', views.chinese_valentines_day, name='campaign.chinese.valentines.day'),
    url(r'^campaign/chinese-valentines-day/participate/$',
        views.chinese_valentines_day_participate, name='campaign.chinese.valentines.day.participate'),
    url(r'^campaign/chinese-valentines-day/result/$',
        views.chinese_valentines_day_result, name='campaign.chinese.valentines.day.result'),
    url(r'^campaign/every-moment/$', views.every_moment, name='campaign.every.moment'),
    url(r'^campaign/every-moment/upload/$', views.every_moment_upload, name='campaign.every.moment.upload'),
    url(r'^campaign/every-moment/exceed/$', views.every_moment_exceed, name='campaign.every.moment.exceed'),
    url(r'^campaign/every-moment/result/$', views.every_moment_result, name='campaign.every.moment.result'),
    url(r'^campaign/every-moment/wall/$', views.every_moment_wall, name='campaign.every.moment.wall'),
    url(r'^campaign/every-moment/wall/(?P<page_number>\d+)/$', views.every_moment_wall_page,
        name='campaign.every.moment.wall.page'),
    url(r'^campaign/10years/firefox-family-award/ticket/$', views.firefox_family_get_ticket),
    url(r'^campaign/10years/firefox-family-award/lottery/$', views.firefox_family_lottery),
    url(r'^campaign/10years/firefox-family/validate/', views.firefox_day_verify, {'template': 'event/10years/firefox-day-verify.html'}),
    url(r'^campaign/10years/browser-survey/claim-award/$', views.campaign_claim_award,
        {'campaign_slug': '10years-survey', 'award_name': u'抽獎', 'nav_template': 'event/10years/navigator.html'},
        name='campaign.10years.browser.survey.claim.award'),
    url(r'^campaign/10years/firefox-family/claim-award/$', views.campaign_claim_award,
        {'campaign_slug': '10years', 'award_name': u'幸運轉輪', 'nav_template': 'event/10years/navigator.html'},
        name='campaign.10years.firefox.family.claim.award'),
    url(r'^events/attack-on-web/$', views.attack_on_web, name='event.attack.on.web'),
    url(r'^events/attack-on-web/prizes/$', views.prizes, name='event.attack.on.web.prizes'),
    url(r'^events/attack-on-web/apply/$', views.apply, name='event.attack.on.web.apply'),
    url(r'^events/attack-on-web/demo/$', views.demo, name='event.attack.on.web.demo'),
    url(r'^events/attack-on-web/demo/app/'
        r'(?P<app_name>(?i)foxmosa-draw-fortune|attack-on-clock|foxcam|shotnote)_(?P<app_id>[1-4])/$',
        views.demo, name='event.attack.on.web.demo.app'),
    url(r'^events/attack-on-web/microfilm/$', views.microfilm, name='event.attack.on.web.microfilm'),
    url(r'^events/microfilm-vote/$', views.microfilm_vote, name='event.microfilm'),
    url(r'^events/microfilm-vote/video/(?P<video_id>[1-4])/$', views.microfilm_vote_video,
        name='event.microfilm.vote.video'),
    url(r'^api/recent_events/$', views.list_recent_events),
)
