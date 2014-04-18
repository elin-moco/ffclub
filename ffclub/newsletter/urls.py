from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns(
    '',
    url(r'^api/newsletter/$', views.newsletter, name='newsletter.list'),
    url(r'^api/newsletter/(?P<page_number>\d+)$', views.newsletter, name='newsletter.list.page'),
    url('^api/newsletter/subscriptions/count$', views.subscription_count),
    url('^api/newsletter/subscribed$', views.subscribed),
    url('^api/newsletter/subscribe$', views.subscribe),
    url('^api/newsletter/unsubscribe$', views.unsubscribe),

)
