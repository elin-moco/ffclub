from django.conf.urls.defaults import *

from django.views.generic.simple import direct_to_template

urlpatterns = patterns(
    '',
    url(r'^tos/$', direct_to_template, {'template': 'tos.html'}, name='tos'),
)
